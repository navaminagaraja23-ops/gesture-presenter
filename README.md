# Gesture Presenter

A touch-free presentation controller. It uses a webcam to recognise hand gestures and sends keyboard commands to Google Slides or PowerPoint.

## The problem
Presenters have to stay next to the laptop or hold a clicker to change slides. Gesture Presenter lets you control slides from a distance with your hand.

## Gestures
| Gesture | Command |
|---|---|
| Fist (hold 1.5s) | Lock / unlock |
| Index finger | Next slide |
| Index + middle fingers | Previous slide |
| Three fingers | Black screen on/off |
| Pinky only | End slideshow |
| Thumbs up | First slide |
| Open palm (hold 1s) | Mute / unmute |

Gestures only work after unlocking. Each one must be held briefly, so unclear movements do not trigger anything by accident.

## How to run
1. Install Python 3.11.
2. `pip install -r requirements.txt`
3. `python main.py`
4. Open a slideshow, click on it, then unlock with the fist.
5. Press Esc in the webcam window to quit.

## Built with
Python, MediaPipe, OpenCV, PyAutoGUI

## Team
Yashash M Gowda,
Yashwanth P,
Navami G N,
Rakshitha M V .

