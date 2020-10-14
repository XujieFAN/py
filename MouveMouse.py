import pyautogui

while pyautogui.position().x < 700:
    pyautogui.moveTo(500, 500, duration=5)
    pyautogui.click()
    pyautogui.moveTo(400, 600, duration=5)
    pyautogui.click()
