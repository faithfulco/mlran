# MLRan: A Behavioural Dataset for Ransomware Analysis and Detection

[![JNCA](https://img.shields.io/badge/arXiv-2505.18613-b31b1b.svg)](https://www.sciencedirect.com/science/article/pii/S1084804526000500)

**MLRan** is a large-scale, high-quality behavioural dataset designed to support research in machine learning-based ransomware detection, classification, and behavioural analysis. The dataset comprises **over 4,800 dynamically analysed samples**, spanning **64 ransomware families** and a **balanced set of goodware**, collected between **2006 and 2024**. The dataset covers all major ransomware types, including locker, crypto, ransomware-as-a-service (RaaS), and modern variants.

MLRan follows **GUIDE-MLRan**, a set of practical guidelines we propose for constructing high-quality behavioural ransomware datasets. The repository provides open access to the dataset (feature-processed), collection and parsing scripts, machine learning pipelines, and interpretability experiments, all designed to ensure reproducibility and transparency.

You can read more about the dataset in the published paper in the Elsevier Journal of Network and Computer Applications: [Read the paper](https://www.sciencedirect.com/science/article/pii/S1084804526000500)

## Resources

📂 **Complete Dataset on (Zenodo):** [Access the complete MLRan dataset](https://zenodo.org/records/23403681)

💻 **Codebase (GitHub):** [MLRan Source Code](https://github.com/faithfulco/mlran)

📄 **Research Paper (Journal of Network and Computer Applications):** [https://doi.org/10.1016/j.jnca.2026.104475](https://doi.org/10.1016/j.jnca.2026.104475)


## Citation

Please cite the following if you use MLRan in your work:

Onwuegbuche, F. C., Adelodun, S. O., Jurcut, A. D., & Pasquale, L. (2026). MLRan: A behavioural dataset for ransomware analysis and detection. Journal of Network and Computer Applications, 104475.

```bibtex
@article{onwuegbuche2026mlran,
  title={{MLRan}: A behavioural dataset for ransomware analysis and detection},
  author={Onwuegbuche, Faithful Chiagoziem and Adelodun, Sunday Olaoluwa and Jurcut, Anca Delia and Pasquale, Liliana},
  journal={Journal of Network and Computer Applications},
  pages={104475},
  year={2026},
  publisher={Elsevier},
  doi={10.1016/j.jnca.2026.104475}
}
```

## Project Overview
The figure below summarises the MLRan pipeline, from sample collection and dynamic analysis to feature extraction, selection, and ML-based classification with SHAP and LIME explainability.

![model_design](https://github.com/user-attachments/assets/cb17acf3-5c2f-4d75-8dfc-771b35eaa523)


## Repository Structure

```
mlran/
│
├── 1_sample_collection_scripts/       # Scripts to collect goodware and ransomware samples
├── 2_collected_samples_metadata/      # Metadata associated with each analysed sample
├── 3_cuckoo_submission_automation/    # Scripts for automated Cuckoo submission and report extraction
├── 4_cuckoo_parser_scripts/           # Parsers for extracting behavioural features from Cuckoo reports
├── 5_mlran_dataset/                   # Information and links to the full MLRan dataset
├── 6_experiments/                     # ML experiments, feature selection, evaluation, results and feature selected dataset
├── LICENSE
└── README.md
```

## Key Statistics

| Property                     | Value              |
| ---------------------------- | ------------------ |
| Total Samples                | 4,800+             |
| Ransomware Families          | 64                 |
| Time Range                   | 2006–2024          |
| Feature Space (raw)          | 6.4 million+       |
| Feature Space (reduced)      | 483 (via MI + RFE) |
| Max Accuracy (ML)            | 98.7%              |
| Max Precision / Recall       | 98.9% / 98.5%      |

## Disclaimer

All ransomware analyses were conducted in **controlled sandbox environments**. This repository **does not distribute raw binaries**. However, we provide sample hashes and complete metadata, including code to help you download the samples. Researchers should follow appropriate safety protocols when working with malware and comply with their institution’s ethical and legal standards.

## Contact

- **Lead Author**: [Faithful Chiagoziem Onwuegbuche](https://github.com/faithfulco)  
- 📧 Email: [faithful.onwuegbuche@ucd.ie](mailto:faithful.onwuegbuche@ucd.ie)  
- 🔗 LinkedIn: [faithful-onwuegbuche](https://www.linkedin.com/in/faithful-onwuegbuche/)  

## License

This repository is licensed under the [MIT License](LICENSE). Attribution is appreciated.
