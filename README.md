# Autofocus for the 16mm telephoto lens mounted on a Raspberry Pi HQ Camera.
As you may have already noticed, the Raspberry Pi HQ Camera lenses don't have any autofocus functionality. This project includes the hardware design, firmware and software to add autofocus functionality to those lenses. In this case, I use the 16mm telephoto lens.
The project is divided into two repositories. This repository includes the code of the M5Stack firmware whereas [lemariva/rPIFocus](https://github.com/lemariva/rPIFocus) includes the code for the Raspberry Pi, in which the Microservices application runs.

A detailed article about the application can be found on [Raspberry Pi HQ Camera: Autofocus for the Telephoto Lens (JiJi)](https://lemariva.com/blog/2020/12/raspberry-pi-hq-camera-autofocus-telephoto-lens).

## Video
[![Autofocus for the Raspberry HQ Camera](https://img.youtube.com/vi/PrbyPmq_Z7Q/0.jpg)](https://www.youtube.com/watch?v=PrbyPmq_Z7Q)

## Photo examples
|          |          |          |          |
|:--------:|:--------:|:--------:|:--------:|
|<img src="https://lemariva.com/storage/app/uploads/public/5fe/c63/443/5fec63443a76c981023585.jpg" alt="Focus Type: Box - Background focused" width="300px">|<img src="https://lemariva.com/storage/app/uploads/public/5fe/c63/392/5fec6339224b0320000410.jpg" alt="Focus Type: Box - Nanoblock bird focused" width="300px">|<img src="https://lemariva.com/storage/app/uploads/public/5fe/c63/4ab/5fec634ab3092068212455.jpg" alt="Focus Type: Box - Nanoblock bird focused. Diff. illum & cam. aperture" width="300px">|<img src="https://lemariva.com/storage/app/uploads/public/5fe/c63/3cd/5fec633cda6af591369087.jpg" alt="Focus Type: Object detector - Teddy bear focused" width="300px">|
|Focus Type: Box <br/> Background focused (<a href="https://lemariva.com/storage/app/media/blog_imgs/hqcamera/hq_camera_background_focused.jpg">download</a>)|Focus Type: Box <br/>Nanoblock bird focused (<a href="https://lemariva.com/storage/app/media/blog_imgs/hqcamera/hq_camera_nanoblock_bird_focused.jpg">download</a>)|Focus Type: Box <br/>Nanoblock bird focused. <br/> Diff. illum & cam. aperture (<a href="https://lemariva.com/storage/app/media/blog_imgs/hqcamera/hq_camera_nanoblock_bird_focused_2.jpg">download</a>)|Focus Type: Object detector  <br/>Teddy bear focused (<a href="https://lemariva.com/storage/app/media/blog_imgs/hqcamera/hq_camera_teddy_bear_focused.jpg">download</a>)|

## Simple PCB schematic
Inside the folder [`pcb`](https://github.com/lemariva/rPIFocus/tree/main/pcb), you'll find the board and schematic files (Eagle), to order your PCB. I also added the Gerber files that I used by <a rel="noopener noreferrer" href="https://jlcpcb.com/">jlcpcb</a>.

## M5Stack Application
The M5Stack ATOM Matrix controls the motors and offers a RestAPI to receive the commands. The M5Stack application is programmed in MicroPython. If you haven't heard about MicroPython, you can check this tutorial: [Getting Started with MicroPython on ESP32, M5Stack, and ESP8266](https://lemariva.com/blog/2020/03/tutorial-getting-started-micropython-v20). MicroPython is a lean and efficient implementation of the Python 3 programming language that includes a small subset of the Python standard library and is optimized to run on microcontrollers and in "constrained environments".
The application is located [lemariva/uPyFocus](https://github.com/lemariva/uPyFocus). 

So, follow these steps to upload the application to the M5Stack:
1. Flash MicroPython to the M5Stack as described in [this tutorial](https://lemariva.com/blog/2020/03/tutorial-getting-started-micropython-v20).
2. Clone the [lemariva/uPyFocus](https://github.com/lemariva/uPyFocus) repository:
    ```sh
    git clone https://github.com/lemariva/uPyFocus.git
    ```
3. Open the folder `uPyFocus` with <a rel="noopener noreferrer" href="https://code.visualstudio.com/">VSCode</a> and rename the `config.py.sample` to `config.py`. 
4. Open the file and add your Wi-Fi credentials in this section:
    ```python
    wifi = {
        'ssid':'',
        'password':''
    }
    ```
    The M5Stack needs to connect to your Wi-Fi so that the Raspberry Pi (also connected to your Wi-Fi/LAN) can find it and sends the commands to control the steppers.
5. Upload the application to the M5Stack.

After uploading the code, the M5Stack resets and starts with the calibration routine. Take note of the IP that the M5Stack reports while connecting to your Wi-Fi. You'll need that to configure the Microservices Application on the Raspberry Pi.