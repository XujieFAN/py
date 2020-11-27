import pyautogui

while pyautogui.position().x < 1000:
    pyautogui.moveTo(600, 500, duration=5)
    pyautogui.click()
    pyautogui.moveTo(600, 600, duration=5)
    pyautogui.click()
