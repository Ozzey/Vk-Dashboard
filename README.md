# VKontakte Scoial Media Analytical Dashboard


## How To Use:
****************************************************
### 1.Installing the Libraries:
```bash
pip install -r requirements.txt
```
****************************************************
### 2.Create your VK App [HERE](https://vk.com/editapp?act=create)
Copy your application ID
****************************************************
### 3.Get your Authentication Token from the link below
```bash
https://oauth.vk.com/authorize?client_id={YOUR-APPLICATION-ID-WITHOUT-PARENTHESIS}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131
```
You have to write your application ID that you got from Step-2 in place of:
*{YOUR-APPLICATION-ID-WITHOUT-PARENTHESIS}*
****************************************************
### 4. Open keys.py file:

```bash
keys = {
    "ACCESS_TOKEN" : "YOUR-Access-Token"
    ,
    "user_id" : "Your-Profile-ID (not same as application ID)",
}

```
Replace "YOUR-Access-Token" and "Your-Profile-ID" with relevant information

****************************************************
### 5. OPEN downloader.py file and uncomment everything:
run downloader.py file using
```bash
python downloader.py
```
****************************************************
### 6. After everything is downloaded run index.py using:
```bash
python index.py
```
****************************************************
*SAMPLE Dashboard:*
![Sample](https://user-images.githubusercontent.com/49760167/172894257-132b3447-8204-418b-a854-1f569da6114f.png)


> Live Version of the dashboard will be available soon.
