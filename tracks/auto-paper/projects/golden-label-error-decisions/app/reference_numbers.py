"""Numbers reported by prior work that the paper compares against, with their sources.

Every value was copied from the arXiv text of the cited paper and checked with an exact string search;
page numbers refer to the arXiv PDF version named in each block. Nothing here is computed by this project.
compare.py puts our own measurements next to these values.
"""

# Gema et al., "Are We Done with MMLU?", arXiv 2406.04127v3 (NAACL 2025).
# Table 5 (p18): subject -> (original MMLU size, annotated, OK, BQC, BOC, NCA, MCA, WGT).
GEMA_TABLE5 = {
    "virology": (166, 100, 43, 14, 2, 4, 4, 33),
    "logical fallacies": (163, 100, 74, 14, 2, 4, 3, 3),
    "college chemistry": (100, 100, 75, 2, 0, 2, 0, 21),
    "professional law": (1534, 100, 82, 4, 1, 0, 11, 2),
    "human sexuality": (131, 100, 83, 11, 1, 2, 1, 2),
    "business ethics": (100, 100, 86, 14, 0, 0, 0, 0),
    "formal logic": (126, 100, 87, 1, 0, 2, 9, 1),
    "human aging": (223, 100, 88, 12, 0, 0, 0, 0),
    "global facts": (100, 100, 88, 2, 1, 4, 0, 5),
    "machine learning": (112, 100, 89, 3, 5, 0, 1, 2),
    "miscellaneous": (783, 100, 90, 4, 1, 4, 1, 0),
    "abstract algebra": (100, 100, 91, 2, 0, 1, 0, 6),
    "public relations": (110, 100, 91, 3, 0, 0, 3, 3),
    "high school european history": (165, 100, 91, 4, 4, 0, 0, 1),
    "professional accounting": (282, 100, 94, 0, 1, 5, 0, 0),
    "astronomy": (152, 100, 94, 2, 2, 1, 0, 1),
    "security studies": (245, 100, 94, 6, 0, 0, 0, 0),
    "conceptual physics": (235, 100, 95, 0, 0, 0, 1, 4),
    "international law": (121, 100, 95, 0, 0, 0, 3, 2),
    "high school biology": (310, 100, 95, 1, 1, 1, 0, 2),
    "college medicine": (173, 100, 96, 2, 0, 1, 0, 1),
    "moral disputes": (346, 100, 96, 3, 0, 0, 0, 1),
    "marketing": (234, 100, 96, 2, 2, 0, 0, 0),
    "professional psychology": (612, 100, 96, 1, 0, 1, 0, 2),
    "high school psychology": (545, 100, 96, 4, 0, 0, 0, 0),
    "high school physics": (151, 100, 97, 0, 0, 1, 0, 2),
    "elementary mathematics": (378, 100, 97, 1, 0, 0, 0, 2),
    "high school macroeconomics": (390, 100, 97, 2, 0, 0, 1, 0),
    "college computer science": (100, 100, 97, 0, 0, 2, 1, 0),
    "computer security": (100, 100, 97, 0, 0, 0, 0, 3),
    "moral scenarios": (895, 100, 97, 3, 0, 0, 0, 0),
    "econometrics": (114, 100, 97, 3, 0, 0, 0, 0),
    "nutrition": (306, 100, 98, 1, 1, 0, 0, 0),
    "high school microeconomics": (238, 100, 98, 1, 0, 0, 0, 1),
    "sociology": (201, 100, 98, 2, 0, 0, 0, 0),
    "high school statistics": (216, 100, 98, 0, 0, 0, 0, 2),
    "college biology": (144, 100, 98, 1, 0, 0, 0, 1),
    "electrical engineering": (145, 100, 98, 1, 0, 0, 0, 1),
    "high school world history": (237, 100, 99, 0, 0, 0, 0, 1),
    "anatomy": (135, 100, 99, 0, 0, 0, 0, 1),
    "high school mathematics": (270, 100, 99, 0, 0, 0, 0, 1),
    "high school chemistry": (203, 100, 99, 1, 0, 0, 0, 0),
    "jurisprudence": (108, 100, 99, 0, 1, 0, 0, 0),
    "world religions": (171, 100, 99, 1, 0, 0, 0, 0),
    "us foreign policy": (100, 100, 99, 1, 0, 0, 0, 0),
    "clinical knowledge": (265, 100, 99, 1, 0, 0, 0, 0),
    "professional medicine": (272, 100, 99, 1, 0, 0, 0, 0),
    "college mathematics": (100, 100, 99, 1, 0, 0, 0, 0),
    "management": (103, 100, 100, 0, 0, 0, 0, 0),
    "philosophy": (311, 100, 100, 0, 0, 0, 0, 0),
    "medical genetics": (100, 100, 100, 0, 0, 0, 0, 0),
    "high school us history": (204, 100, 100, 0, 0, 0, 0, 0),
    "high school government and politics": (193, 100, 100, 0, 0, 0, 0, 0),
    "high school geography": (198, 100, 100, 0, 0, 0, 0, 0),
    "high school computer science": (100, 100, 100, 0, 0, 0, 0, 0),
    "college physics": (102, 100, 100, 0, 0, 0, 0, 0),
    "prehistory": (324, 100, 100, 0, 0, 0, 0, 0),
}
GEMA = {
    "error_share_stratified": 0.0649,  # p4: "we estimate that 6.49% of the questions in the complete MMLU dataset contain errors"
    "wgt_share_stratified": 0.0142,    # Table 5 Total row (p18): WGT 1.42%
    # Table 2 (p7): exact match on all HELM instances (rank on the HELM leaderboard) -> on correct Redux
    # instances (rank among the ten models). Virology column, Llama 3.1 Instruct Turbo (405B):
    "virology_llama405b": {"all": (0.57, 16), "correct": (0.93, 1)},
    "table2_models": 10,
    # Fig. 6 (p6): per-model Pearson r between subject exact match and the subject's ratio of correct items.
    "fig6_pearson_range": (0.33, 0.54),
}

# Vendrow et al., "Do Large Language Model Benchmarks Test Reliability?", arXiv 2502.03461v1.
VENDROW = {
    # Table 2 (p4), MMLU high school mathematics: original questions, bad questions, mislabeled.
    "mmlu_hs_math": {"original": 270, "bad": 2, "mislabeled": 0},
    # Table 4 (p7), MMLU HS Math: average number of model errors on the original and the cleaned set,
    # and the share of model errors due to benchmark errors.
    "mmlu_hs_math_errors": {"original": 20.5, "cleaned": 19.5, "benchmark_share": 0.05},
    # Table 4 (p7): benchmark-error share over the 14 benchmarks ranges from 0% to 93%.
    "benchmark_share_range": (0.0, 0.93),
    # p8: their re-labeling agrees with MMLU-Redux on all but one of the 100 shared HS-math items.
    "redux_overlap": {"shared": 100, "disagree": 1},
}

# Northcutt, Athalye, Mueller, "Pervasive Label Errors in Test Sets Destabilize ML Benchmarks",
# arXiv 2103.14749v4 (NeurIPS 2021 Datasets and Benchmarks).
NORTHCUTT = {
    "avg_error_rate": 0.033,  # abstract (p1): "an average of at least 3.3% errors"
    # p8 (Fig. 4 caption): on ImageNet, ResNet-18 overtakes ResNet-50 on corrected labels when the
    # noise prevalence N = |C|/|P| rises from 2.9% to about 9% ("increases by around 6%").
    "imagenet": {"n0": 0.029, "n_flip": 0.09, "increase": 0.06},
    # abstract (p1): on CIFAR-10, VGG-11 overtakes VGG-19 when the prevalence increases by 5%; N0 = 0.2% (Fig. 5).
    "cifar10": {"n0": 0.002, "increase": 0.05},
    # p6: models that do best on the original labels of the correctable set do worst on its corrected labels;
    # p7: NASNet-large drops from rank 1/34 to 29/34 on ImageNet's correctable set.
}

# Madaan et al., "Quantifying Variance in Evaluation Benchmarks", arXiv 2406.10229v1.
MADAAN = {
    # Table 1 (p4), MMLU: seed std E(S,M) over ten 7B models (at chance, mean 25.86%) and the 95% CI width.
    "mmlu_seed_std_pp": 0.57, "mmlu_ci95_pp": 0.72, "mmlu_mean_acc": 25.86,
    # p9: on 100-item IRT subsets, Kendall tau with the full set can drop to 0.76, i.e. 12% of pairwise
    # comparisons reverse; Table 7 (p22) gives 4.51% (GSM8k) to 12.17% (ARC-C) for IRT subsets.
    "subset100_pair_flip_range": (0.0451, 0.1217),
}

# Card et al., "With Little Power Comes Great Responsibility", EMNLP 2020 (arXiv 2010.06595v1).
CARD = {
    # Table 2 (p5): estimated minimum detectable effect (accuracy points) at 80% power.
    "mde_pp": {"WNLI": (147, 5.26), "MRPC": (1725, 1.62), "QNLI": (5463, 0.55)},
}

# Alzahrani et al., "When Benchmarks are Targets", ACL 2024 (arXiv 2402.01781v2).
ALZAHRANI = {
    "max_rank_shift": 8,          # abstract (p1): rankings change "up to 8 positions"
    "answer_shuffle": {"models": 11, "changed": 5, "ktau": 0.564},  # p6, MMLU answer-order shuffle
}
