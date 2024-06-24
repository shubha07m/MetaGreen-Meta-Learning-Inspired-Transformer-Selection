## Meta-Learning Inspired Transformer Selection for Green Semantic Communication

![End to end image/text transformer based SemCom with communication channel](https://github.com/shubha07m/MetaGreen/blob/main/semcom_transformers.png)
Semantic Communication focuses on transmitting meaningful and effective content instead of just individual symbols or bits. This method promises to reduce latency, lower bandwidth usage, and increase throughput compared to traditional communication methods. However, a key challenge is the lack of universal metrics to measure both semantic information loss and energy consumption.

This research introduces an innovative solution: the “Energy-Optimized Semantic Loss” (EOSL) function. EOSL is a multi-objective loss function that balances semantic information loss with energy consumption. Through extensive experiments with transformer models, including energy benchmarking, EOSL-based model selection has been shown to improve the similarity-to-power ratio (SPR) by up to 83% compared to BLEU score-based selection and by 67% compared to selecting models based solely on the lowest power usage.

![Avg. Similarity vs. Avg. Power Performance Comparison of Metrics](https://github.com/shubha07m/MetaGreen/blob/main/bleu_comparison.png)

Additionally, EOSL's applicability extends to various contexts using Meta-Learning principles. By using cumulative EOSL values, the model selection system can adapt over time, making it more energy-efficient. This research lays the groundwork for developing energy-efficient model selection and advancing green semantic communication.

![Variation of topic contex of images](https://github.com/shubha07m/MetaGreen/blob/main/contexts.png)

