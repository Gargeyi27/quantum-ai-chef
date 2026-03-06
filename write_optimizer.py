"""Run this script to write optimizer.py correctly: python write_optimizer.py"""

code = '''import numpy as np
import json
import os
from itertools import combinations
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")


class QuantumState:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.dim = 2 ** n_qubits
        self.state = np.ones(self.dim, dtype=complex) / np.sqrt(self.dim)

    def apply_cost_unitary(self, H_C, gamma):
        self.state *= np.exp(-1j * gamma * H_C)

    def apply_mixer_unitary(self, beta):
        cos_b = np.cos(beta)
        sin_b = np.sin(beta)
        for qubit in range(self.n):
            new_state = np.zeros(self.dim, dtype=complex)
            for s in range(self.dim):
                f = s ^ (1 << qubit)
                new_state[s] += cos_b * self.state[s]
                new_state[s] -= 1j * sin_b * self.state[f]
            self.state = new_state

    def measure_expectation(self, H_C):
        probs = np.abs(self.state) ** 2
        return float(np.dot(probs, H_C))

    def sample(self, n_shots=1000):
        probs = np.abs(self.state) ** 2
        probs = probs / probs.sum()
        indices = np.random.choice(self.dim, size=n_shots, p=probs)
        counts = {}
        for idx in indices:
            bits = format(idx, f"0{self.n}b")
            counts[bits] = counts.get(bits, 0) + 1
        return counts


class QUBOFormulator:
    def __init__(self, alpha=1.0, beta=0.5, gamma=0.8, delta=0.7):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

    def build_ising_hamiltonian(self, ingredients, clash_matrix, nutrition_scores, K=6, fusion_flags=None):
        n = len(ingredients)
        dim = 2 ** n
        H_diag = np.zeros(dim)
        for state_idx in range(dim):
            bits = [(state_idx >> i) & 1 for i in range(n)]
            energy = 0.0
            for i, j in combinations(range(n), 2):
                if bits[i] and bits[j]:
                    energy += self.alpha * clash_matrix[i, j]
            for i in range(n):
                if bits[i]:
                    energy += self.beta * nutrition_scores[i]
            n_selected = sum(bits)
            energy += self.gamma * (n_selected - K) ** 2
            if fusion_flags is not None:
                c1 = sum(bits[i] * fusion_flags[i][0] for i in range(n))
                c2 = sum(bits[i] * fusion_flags[i][1] for i in range(n))
                if c1 + c2 > 0:
                    balance = abs(c1 - c2) / (c1 + c2 + 1e-6)
                    energy += self.delta * balance
            H_diag[state_idx] = energy
        return H_diag


class QAOAOptimizer:
    def __init__(self, p_layers=3):
        self.p = p_layers

    def _evaluate(self, H_C, n_qubits, gammas, betas):
        qs = QuantumState(n_qubits)
        for layer in range(self.p):
            qs.apply_cost_unitary(H_C, gammas[layer])
            qs.apply_mixer_unitary(betas[layer])
        return qs.measure_expectation(H_C)

    def _sample(self, H_C, n_qubits, gammas, betas, n_shots=2000):
        qs = QuantumState(n_qubits)
        for layer in range(self.p):
            qs.apply_cost_unitary(H_C, gammas[layer])
            qs.apply_mixer_unitary(betas[layer])
        return qs.sample(n_shots)

    def optimize(self, H_C, n_qubits, n_iterations=50):
        gammas = np.random.uniform(0, np.pi, self.p)
        betas = np.random.uniform(0, np.pi / 2, self.p)
        best_energy = float("inf")
        best_angles = (gammas.copy(), betas.copy())
        for iteration in range(n_iterations):
            for layer in range(self.p):
                for param_type in ["gamma", "beta"]:
                    d = 0.1 * np.exp(-iteration / 30)
                    if param_type == "gamma":
                        gammas[layer] += d
                        ep = self._evaluate(H_C, n_qubits, gammas, betas)
                        gammas[layer] -= 2 * d
                        em = self._evaluate(H_C, n_qubits, gammas, betas)
                        gammas[layer] += d
                        gammas[layer] -= 0.05 * (ep - em) / (2 * d)
                    else:
                        betas[layer] += d
                        ep = self._evaluate(H_C, n_qubits, gammas, betas)
                        betas[layer] -= 2 * d
                        em = self._evaluate(H_C, n_qubits, gammas, betas)
                        betas[layer] += d
                        betas[layer] -= 0.05 * (ep - em) / (2 * d)
            energy = self._evaluate(H_C, n_qubits, gammas, betas)
            if energy < best_energy:
                best_energy = energy
                best_angles = (gammas.copy(), betas.copy())
        final_counts = self._sample(H_C, n_qubits, *best_angles, n_shots=2000)
        return best_angles, final_counts


class QuantumIngredientsOptimizer:
    def __init__(self, data_path):
        with open(data_path) as f:
            self.data = json.load(f)
        self.cache_path = os.path.join(os.path.dirname(data_path), "quantum_cache.json")
        self.cache = self._load_cache()
        self.qubo = QUBOFormulator()
        self.qaoa = QAOAOptimizer(p_layers=3)

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path) as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_path, "w") as f:
            json.dump(self.cache, f, indent=2)

    def _get_cache_key(self, cuisine1, cuisine2, veg):
        parts = sorted([cuisine1, cuisine2]) if cuisine2 else [cuisine1]
        parts.append("veg" if veg else "nonveg")
        return "_".join(parts)

    def get_optimized_ingredients(self, cuisine1, cuisine2, veg, dish_hint, max_ingredients=8):
        cache_key = self._get_cache_key(cuisine1, cuisine2, veg)
        if cache_key in self.cache:
            result = self.cache[cache_key].copy()
            result["source"] = "quantum_cache"
            return result
        result = self._run_quantum_optimization(cuisine1, cuisine2, veg, max_ingredients)
        self.cache[cache_key] = result
        self._save_cache()
        result["source"] = "quantum_computed"
        return result

    def _run_quantum_optimization(self, cuisine1, cuisine2, veg, K):
        all_ingredients = self.data["ingredients"]
        candidates = []
        for name, info in all_ingredients.items():
            if veg and name in ["chicken", "beef", "salmon", "fish_sauce"]:
                continue
            score = 0
            if cuisine1 in info["cuisines"]:
                score += 2
            if cuisine2 and cuisine2 in info["cuisines"]:
                score += 2
            if info["difficulty"] == 1:
                score += 1
            candidates.append((name, info, score))
        candidates.sort(key=lambda x: -x[2])
        top_candidates = candidates[:12]
        ingredient_names = [c[0] for c in top_candidates]
        n = len(ingredient_names)
        clash_matrix = np.zeros((n, n))
        flavor_clash_pairs = {
            ("sweet", "salty"): -0.3,
            ("acidic", "creamy"): -0.4,
            ("hot", "creamy"): -0.2,
            ("pungent", "pungent"): 0.5,
            ("earthy", "citrus"): 0.3,
        }
        for i in range(n):
            for j in range(i + 1, n):
                fi = set(top_candidates[i][1].get("flavor_profile", []))
                fj = set(top_candidates[j][1].get("flavor_profile", []))
                clash = 0.0
                for (f1, f2), val in flavor_clash_pairs.items():
                    if (f1 in fi and f2 in fj) or (f2 in fi and f1 in fj):
                        clash += val
                clash_matrix[i, j] = clash
                clash_matrix[j, i] = clash
        nutrition_scores = np.array([
            c[1]["nutrition"].get("fat", 0) * 0.01 +
            (1 - min(c[1]["nutrition"].get("fiber", 0) / 10, 1)) * 0.2
            for c in top_candidates
        ])
        fusion_flags = np.array([
            [
                1 if cuisine1 in c[1]["cuisines"] else 0,
                1 if (cuisine2 and cuisine2 in c[1]["cuisines"]) else 0
            ]
            for c in top_candidates
        ])
        H_C = self.qubo.build_ising_hamiltonian(
            ingredient_names, clash_matrix, nutrition_scores,
            K=min(K, n), fusion_flags=fusion_flags
        )
        _, counts = self.qaoa.optimize(H_C, n, n_iterations=40)
        best_bits = min(counts.keys(), key=lambda b: H_C[int(b, 2)])
        selected = [ingredient_names[i] for i, b in enumerate(best_bits) if b == "1"]
        if len(selected) < 4:
            for name, _, _ in top_candidates:
                if name not in selected:
                    selected.append(name)
                if len(selected) >= K:
                    break
        fusion_score = 0.0
        if cuisine2:
            key1 = f"{cuisine1}_{cuisine2}"
            key2 = f"{cuisine2}_{cuisine1}"
            compat = self.data["fusion_compatibility"]
            fusion_score = compat.get(key1, compat.get(key2, 0.75))
        return {
            "selected_ingredients": selected[:K],
            "all_candidates": ingredient_names,
            "fusion_score": round(fusion_score, 3),
            "optimization_method": "QAOA_p3_Ising",
            "n_qubits_used": n
        }


def grover_constraint_search(candidate_configs, constraints):
    if not candidate_configs:
        return []

    def oracle(config):
        if constraints.get("veg") and any(
            ing in ["chicken", "beef", "salmon", "fish_sauce"]
            for ing in config.get("ingredients", [])
        ):
            return False
        if constraints.get("max_ingredients") and len(config.get("ingredients", [])) > constraints["max_ingredients"]:
            return False
        return True

    valid = [c for c in candidate_configs if oracle(c)]
    return valid if valid else candidate_configs[:3]


def vqe_taste_nutrition_tradeoff(ingredients, ingredient_data, taste_weight=0.6, health_weight=0.4):
    if not ingredients:
        return 0.0, "balanced"
    total_taste = 0.0
    total_health = 0.0
    for ing in ingredients:
        if ing in ingredient_data:
            info = ingredient_data[ing]
            nut = info["nutrition"]
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
'''

import os
output_path = os.path.join("quantum_engine", "optimizer.py")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Written to {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")

# Verify it works
import ast
with open(output_path, encoding="utf-8") as f:
    source = f.read()
ast.parse(source)
print("Syntax check passed!")

import importlib.util
spec = importlib.util.spec_from_file_location("optimizer", output_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print("Classes found:", [x for x in dir(mod) if not x.startswith("_")])