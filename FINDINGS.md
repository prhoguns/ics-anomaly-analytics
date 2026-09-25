# Findings

The selected test file contains **43,201 seconds**, including **629 labeled attack seconds** across **five contiguous episodes**. The separate training file contains 216,001 normal seconds. [Split summary](results/01_split_overview.md) · [Episodes](results/02_attack_episodes.md)

1. **Attacks occur in short intervals.** The five test episodes last 60–192 seconds each. The first begins at 2020-07-07 15:35:11 in the dataset clock. [Episode table](results/02_attack_episodes.md)
2. **A basic maximum-z threshold creates a very different review burden at each setting.** At z ≥ 3, it flags 4,735 seconds and finds 77.42% of attack seconds. At z ≥ 5, it flags 578 seconds and finds 72.66%. [Threshold table](results/09_threshold_tradeoff.md)
3. **Normal-range violations can guide triage, but individual sensor spikes need context.** The [sensor-by-label table](results/06_outside_normal_range.md) shows how often test readings fall outside the training 1st–99th percentile for each channel.

## Limits

These figures cover only `train1` and `test1` of HAI 21.03. The training and test files are distinct plant runs; raw z-scores ignore operating mode and sensor coupling. Percentages in the threshold table count seconds, not full attack episodes or time to detection. The labels identify attacks in this testbed and do not prove a given sensor reading is malicious.
