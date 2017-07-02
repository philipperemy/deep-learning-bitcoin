# When Bitcoin meets Artifial Intelligence
[![license](https://img.shields.io/badge/License-Apache_2.0-brightgreen.svg)](https://github.com/philipperemy/keras-attention-mechanism/blob/master/LICENSE) 
[![dep2](https://img.shields.io/badge/Keras-2.0+-brightgreen.svg)](https://keras.io/) 
[![dep2](https://img.shields.io/badge/NVIDIA_Digits-5.0+-brightgreen.svg)](https://github.com/NVIDIA/DIGITS/releases) 
[![dep1](https://img.shields.io/badge/Status-Work_In_Progress-orange.svg)](https://www.tensorflow.org/) 

Exploiting Bitcoin prices patterns with Deep Learning. Like OpenAI, we train our models on raw pixel data. Exactly how an experienced human would see the curves and takes an action.

<p align="center">
  <img src="https://bitcoin.org/img/icons/opengraph.png" width="100">
</p>

So far, we achieved:

- [x] Download Bitcoin tick data
- [x] Convert to 5-minute data
- [x] Convert to Open High Low Close representation
- [x] Train a simple AlexNet on 20,000 samples: accuracy is 70% for predicting if asset will go UP or DOWN
- [ ] Quantify how much the price will go UP or DOWN. Because the price can go UP by epsilon percent 99% of the time, and pulls back by 50%
- [ ] Train on **1,000,000+** samples (at least)
- [ ] Apply more complex Conv Nets (at least Google LeNet)
- [ ] Integrate bar volumes on the generated OHLC (Open, High, Low, Close) image
- [ ] Use CNN attention to know what's important for which image. Maybe only a fraction of the image matters for the prediction

## Results on 20,000 samples (small dataset)

<p align="center">
  <img src="assets/1.png" width="500">
  <br><i>Training on 5 minute price data (Coinbase USD)</i>
</p>

<hr/>

<p align="center">
  <img src="assets/2.png" width="500">
  <br><i>Some examples of the training set</i>
</p>

<hr/>
