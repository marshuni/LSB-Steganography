# LSB-Steganography
A simple tool to steganography texts/images into images using the Least Significant Bit. Based on Python.

# 中文说明

LSB隐写脚本：该脚本可以将图片或文字隐藏入载体图像的最低有效位。相比传统的LSB隐写，增加了以下特性：

- 将文字渲染成图片再隐藏，有效增加了信息的鲁棒性。在部分涂画、遮挡、水印等干扰下，仍能较为有效地还原并辨认出原本的信息。
- 通过异或随机数组的处理，将载体图像的最低位打乱，降低被察觉的可能性。尤其是当载体图像具有较多纹理与噪点时，隐蔽性较好。同时通过指定随机数种子，也能起到类似加密的效果。

以下是该隐写脚本的一些局限性。

- 被隐写图像的宽高信息编码后存储在载体图像的头部，若图像头部被修改，或图象被整体修改(如调整亮度、对比度)，则信息无法读取。
- 无法保证信息的绝对安全。在知晓算法的情况下，使用穷举法枚举随机数种子可能破译出信息。

## 功能介绍

### hide - 将信息隐藏入图片

```shell
python main.py hide <img_file> <payload_file> <mode> <seed>
```

- `<img_file>`: 载体图像。图像越大，则理论能够容纳的信息越多。要求格式未经压缩的图像，如png, bmp等。
- `<payload_file>`: 需要隐写的信息。可以是.txt文本文档或是.png图像。
- `<mode>`: 使用的隐写模式。目前支持`binary`和`gray`两种。
  - `binary`: 将信息以二值化图像的形式存储入载体图像中。适合用于存储文本内容。使用该方法能存储更多信息。
  - `gray`: 将信息以灰度图像的形式写入，适合存储图像内容或低分辨率文字。该方法能够保留更多的细节，便于辨认。
- `<seed>`: 使用的随机数种子，为一个整数。在提取信息时需要输入相同的数字。

### extract - 从含有隐写信息的图片中取出信息

``` shell
main.py extract <stego_file> <output_file> <mode> <seed>
```

- `<stego_file>`: 藏有隐写信息的图像文件。
- `<output_file>`: 指定输出文件的位置和文件名。

## 快速上手

### 安装

- 在终端中使用命令`git clone https://github.com/marshuni/LSB-Steganography.git `命令将代码仓库克隆到本地。

- 进入仓库目录，使用命令`pip install -r requirements.txt`安装程序依赖。

### 隐写

- 运行`python main.py hide ./Example/carrier.png ./Example/payload.txt binary 20230508`
  - 该命令可将`payload.txt`中的文字渲染成二值化的图像并隐写入载体图片中，生成名为`carrier-steg-binary.png`的图片。
  - `20230508` 是用于混淆隐写内容的随机数种子，在取出信息时需要相同的种子。
- 运行`python main.py hide ./Example/carrier.png ./Example/payload.png gray 20230508`
  - 该命令可将payload.png图片以灰度模式隐藏入载体图片中，并生成名为`carrier-steg-gray.png`的图片。

### 取出信息

- 运行`python main.py extract ./Example/carrier-steg-gray.png ./Example/output-pic.png gray 20230508`
  - 该命令可将载体图像中的图片取出，并存储到`output-pic.png`这一文件中。
- 运行`python main.py extract ./Example/carrier-steg-binary.png ./Example/output-text.png binary 20230508`
  - 该命令可将载体图像中写有文字的图片取出，并存储到`output-text.png`这一文件中。

​		
