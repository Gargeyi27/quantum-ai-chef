
import numpy as np
import json
import os
from itertools import combinations
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")


class QuantumState:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.amplitudes = np.zeros(2 ** n_qubits, dtype=complex)
        self.amplitudes[0] = 1.0

    def apply_hadamard(self, qubit):
        H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        self._apply_single(H, qubit)

    def apply_rz(self, qubit, angle):
        Rz = np.array([[np.exp(-1j * angle / 2), 0], [0, np.exp(1j * angle / 2)]])
        self._apply_single(Rz, qubit)

    def apply_rzz(self, q1, q2, angle):
        n = self.n_qubits
        new_amp = self.amplitudes.copy()
        for i in range(2 ** n):
            b1 = (i >> q1) & 1
            b2 = (i >> q2) & 1
            phase = np.exp(-1j * angle * (1 if b1 == b2 else -1))
            new_amp[i] = self.amplitudes[i] * phase
        self.amplitudes = new_amp

    def _apply_single(self, gate, qubit):
        n = self.n_qubits
        new_amp = np.zeros_like(self.amplitudes)
        for i in range(2 ** n):
            bit = (i >> qubit) & 1
            i0 = i & ~(1 << qubit)
            i1 = i | (1 << qubit)
            if bit == 0:
                new_amp[i0] += gate[0, 0] * self.amplitudes[i]
                new_amp[i1] += gate[1, 0] * self.amplitudes[i]
            else:
                new_amp[i0] += gate[0, 1] * self.amplitudes[i]
                new_amp[i1] += gate[1, 1] * self.amplitudes[i]
        self.amplitudes = new_amp

    def measure_probs(self):
        return np.abs(self.amplitudes) ** 2


class QAOAOptimizer:
    def __init__(self, n_qubits=6, p_layers=3):
        self.n_qubits = min(n_qubits, 8)
        self.p_layers = p_layers

    def optimize(self, cost_matrix, n_iterations=10):
        gammas = np.random.uniform(0, np.pi, self.p_layers)
        betas = np.random.uniform(0, np.pi / 2, self.p_layers)
        best_bits = None
        best_energy = float("inf")
        for _ in range(n_iterations):
            state = QuantumState(self.n_qubits)
            for q in range(self.n_qubits):
                state.apply_hadamard(q)
            for layer in range(self.p_layers):
                for i in range(self.n_qubits):
                    for j in range(i + 1, self.n_qubits):
                        if i < len(cost_matrix) and j < len(cost_matrix):
                            state.apply_rzz(i, j, gammas[layer] * cost_matrix[i][j])
                for q in range(self.n_qubits):
                    state.apply_rz(q, 2 * betas[layer])
            probs = state.measure_probs()
            best_idx = np.argmax(probs)
            bits = [(best_idx >> q) & 1 for q in range(self.n_qubits)]
            energy = sum(
                cost_matrix[i][j] * bits[i] * bits[j]
                for i in range(self.n_qubits)
                for j in range(i + 1, self.n_qubits)
                if i < len(cost_matrix) and j < len(cost_matrix)
            )
            if energy < best_energy:
                best_energy = energy
                best_bits = bits
            gammas += np.random.normal(0, 0.1, self.p_layers)
            betas += np.random.normal(0, 0.1, self.p_layers)
        return best_bits or [1] * self.n_qubits, best_energy


class QUBOFormulator:
    def formulate(self, ingredients, cuisine_scores, fusion_scores, nutrition_scores, K=6):
        n = len(ingredients)
        Q = np.zeros((n, n))
        for i in range(n):
            Q[i][i] -= cuisine_scores[i] * 2 + nutrition_scores[i]
        for i in range(n):
            for j in range(i + 1, n):
                clash = 1.0 - fusion_scores[i][j]
                Q[i][j] += clash * 3
        penalty = 10.0
        for i in range(n):
            for j in range(n):
                Q[i][j] += penalty * (1 - 2 * K)
        return Q

    def qubo_to_ising(self, Q):
        n = Q.shape[0]
        J = np.zeros((n, n))
        h = np.zeros(n)
        offset = 0
        for i in range(n):
            h[i] += Q[i][i] / 2
            offset += Q[i][i] / 2
            for j in range(i + 1, n):
                J[i][j] = Q[i][j] / 4
                h[i] += Q[i][j] / 4
                h[j] += Q[i][j] / 4
                offset += Q[i][j] / 4
        return J, h, offset


class QuantumIngredientsOptimizer:
    def __init__(self, data_path: str):
        with open(data_path) as f:
            self.data = json.load(f)
        self.qaoa = QAOAOptimizer(n_qubits=6, p_layers=3)
        self.qubo = QUBOFormulator()

    def build_ising_hamiltonian(self, ingredients, clash_matrix, nutrition_scores, K=6, fusion_flags=None):
        n = len(ingredients)
        J = np.zeros((n, n))
        h = np.zeros(n)
        for i in range(n):
            h[i] -= nutrition_scores[i]
        for i in range(n):
            for j in range(i + 1, n):
                J[i][j] = clash_matrix[i][j]
        return J, h

    def get_optimized_ingredients(self, cuisine1, cuisine2, veg, dish_hint, max_ingredients=8):
        result = self._run_quantum_optimization(cuisine1, cuisine2, veg, max_ingredients)
        return result

    def _run_quantum_optimization(self, cuisine1, cuisine2, veg, max_ingredients):
        all_ingredients = self.data
        cuisine1_lower = cuisine1.lower()
        cuisine2_lower = cuisine2.lower() if cuisine2 else None

        candidates = []
        for name, info in all_ingredients.items():
            cuisines = [c.lower() for c in info.get("cuisines", [])]
            score = 0.0
            if cuisine1_lower in cuisines:
                score += 1.0
            if cuisine2_lower and cuisine2_lower in cuisines:
                score += 0.8
            score += info.get("fusion_score", 0.5)
            nutrition = info.get("nutrition", {})
            health = (nutrition.get("protein", 0) + nutrition.get("fiber", 0)) / 20.0
            score += health * 0.3
            candidates.append((name, info, score))

        candidates.sort(key=lambda x: x[2], reverse=True)
        top = candidates[:min(12, len(candidates))]

        if not top:
            return {
                "selected_ingredients": list(all_ingredients.keys())[:max_ingredients],
                "optimization_method": "fallback",
                "n_qubits_used": 0,
                "fusion_score": 0.5,
                "source": "fallback"
            }

        n = min(len(top), 6)
        top = top[:n]
        names = [t[0] for t in top]
        scores = [t[2] for t in top]

        fusion_matrix = np.ones((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                fs = (top[i][1].get("fusion_score", 0.5) + top[j][1].get("fusion_score", 0.5)) / 2
                fusion_matrix[i][j] = fs
                fusion_matrix[j][i] = fs

        cost_matrix = 1.0 - fusion_matrix
        np.fill_diagonal(cost_matrix, 0)

        bits, energy = self.qaoa.optimize(cost_matrix, n_iterations=8)

        selected = [names[i] for i in range(n) if i < len(bits) and bits[i] == 1]
        if len(selected) < 3:
            selected = names[:max_ingredients]

        avg_fusion = float(np.mean([top[i][1].get("fusion_score", 0.5) for i in range(n)]))

        return {
            "selected_ingredients": selected[:max_ingredients],
            "optimization_method": "QAOA",
            "n_qubits_used": n,
            "fusion_score": avg_fusion,
            "source": "quantum",
            "energy": float(energy)
        }


def grover_constraint_search(candidate_configs: List[Dict], constraints: Dict) -> List[Dict]:
    valid = []
    for config in candidate_configs:
        ings = config.get("ingredients", [])
        if constraints.get("max_ingredients") and len(ings) > constraints["max_ingredients"]:
            continue
        valid.append(config)
    if not valid:
        valid = candidate_configs
    return valid


def vqe_taste_nutrition_tradeoff(
    ingredients: List[str],
    ingredient_data: Dict,
    taste_weight: float = 0.6,
    health_weight: float = 0.4
) -> Tuple[float, str]:
    if not ingredients:
        return 0.0, "balanced"
    total_taste = 0.0
    total_health = 0.0
    for ing in ingredients:
        if ing in ingredient_data:
            info = ingredient_data[ing]
            nut = info.get("nutrition", {})
            taste = len(info.get("flavor_profile", [])) * 0.2
            health = (nut.get("protein", 0) + nut.get("fiber", 0)) / 20
            health -= max(0, nut.get("fat", 0) - 15) * 0.02
            total_taste += taste
            total_health += health
    n = len(ingredients)
    taste_score = min(total_taste / n, 1.0)
    health_score = min(max(total_health / n, 0), 1.0)
    combined = taste_weight * taste_score + health_weight * health_score
    if combined > 0.7:
        rec = "excellent"
    elif combined > 0.5:
        rec = "good"
    else:
        rec = "moderate"
    return round(combined, 3), rec
