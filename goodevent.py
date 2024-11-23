import requests # type: ignore
import json
import random
from gooey import Gooey, GooeyParser # type: ignore

@Gooey
def main():
    amogus = GooeyParser(description='Upload to multiple accounts at once to good event.')
    amogus.add_argument('Image', help='.JPG ONLY', widget='FileChooser')
    amogus.add_argument('Username1', action="store")
    amogus.add_argument('Password1', action="store")
    amogus.add_argument('--Username2', action="store")
    amogus.add_argument('--Password2', action="store")
    amogus.add_argument('--Username3', action="store")
    amogus.add_argument('--Password3', action="store")
    amogus.add_argument('--Username4', action="store")
    amogus.add_argument('--Password4', action="store")
    amogus.add_argument('ชื่อเรื่อง', action="store")
    amogus.add_argument('สถานที่', action="store")
    amogus.add_argument('รายละเอียด', action="store")
    amogus.add_argument('--เพื่อครอบครัว', action='store_true')
    amogus.add_argument('--เพื่อสถานศึกษา', action='store_true')
    amogus.add_argument('--เพื่อสังคม', action='store_true')

    variables = amogus.parse_args()

    Username=[]
    Username.append(variables.Username1)
    if variables.Username2 != None:
        Username.append(variables.Username2)
    if variables.Username3 != None:
        Username.append(variables.Username3)
    if variables.Username4 != None:
        Username.append(variables.Username4)
    Password=[]
    Password.append(variables.Password1)
    if variables.Password2 != None:
        Password.append(variables.Password2)
    if variables.Password3 != None:
        Password.append(variables.Password3)
    if variables.Password4 != None:
        Password.append(variables.Password4)
    imageFile = variables.Image
    if imageFile.find('.jpg') == -1:
        raise Exception('Nigga this not .jpg')
    # 1 = ครอบครัว     2 = เพื่อสถานศึกษาหรือสถานที่ทำงาน     3 = เพื่อสังคม
    if sum([variables.เพื่อครอบครัว,variables.เพื่อสถานศึกษา,variables.เพื่อสังคม]) > 1:
        raise Exception('nigga select only one เพื่อครอบครัว or เพื่อสถานศึกษา or เพื่อสังคม')
    if sum([variables.เพื่อครอบครัว,variables.เพื่อสถานศึกษา,variables.เพื่อสังคม]) == 0:
        raise Exception('nigga please select at least one เพื่อครอบครัว or เพื่อสถานศึกษา or เพื่อสังคม')
    if variables.เพื่อครอบครัว == True:
        eventID = 1
    elif variables.เพื่อสถานศึกษา == True:
        eventID = 2
    elif variables.เพื่อสังคม == True:
        eventID = 3
    else:
        raise Exception('Something is fucked in the eventID department')
    ชื่อเรื่อง = variables.ชื่อเรื่อง
    สถานที่ = variables.สถานที่
    รายละเอียด = variables.รายละเอียด


    # format goodEvent by ID
    if eventID == 1:
        eventTypeID = '1'
        Name = 'ทำความดีเพื่อครอบครัว'
        Description = 'เป็นการสร้างให้เกิดความสัมพันธ์ในครอบครัวจากการทำความดี'
    elif eventID == 2:
        eventTypeID = '2'
        Name = 'ทำความดีเพื่อสถานศึกษาหรือที่ทำงาน'
        Description = 'เป็นการสร้างให้เกิดความรักความผูกพันธ์ระหว่างบุคคล'
    elif eventID == 3:
        eventTypeID = '3'
        Name = 'ทำความดีเพื่อสังคมส่วนรวม'
        Description = 'ขยายผลการทำความดีไปสู่สังคมสาธารณะ'

    # generate random date
    possibleDays = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
    day = random.choice(possibleDays)
    possibleMonths = ['01','02','03','04','05','06','07','08','09','10']
    month = random.choice(possibleMonths)
    year = '2024'
    possibleHours = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    hour = random.choice(possibleHours)
    possibleMinutes = ['00','10','20','30','40','50']
    minutes = random.choice(possibleMinutes)
    seconds = '00'

    datestr = year +'-'+ month+'-'+day+'T'+hour+':'+minutes+':'+seconds

    for i in range(len(Username)):
        # print("gay")
        # get user token (login)

        url = "https://goodevent.tdc.mi.th/api/v1/auth/signin"

        payload = json.dumps({
        "username": Username[i],
        "password": Password[i]
        })
        headers = {
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'DNT': '1',
        'content-type': 'application/json',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'goodevent.tdc.mi.th'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # get token
        response = response.json()["token"]

        print(response)
        Token = response
        print('authenticated')


        # upload file to cdn

        url = "https://goodevent.tdc.mi.th/api/v1/files/multiple/file"

        payload = {'citizenId': Username[i]}
        files=[
        ('files',('IMG_20240921_171633.jpg',open(imageFile,'rb'),'image/jpeg'))
        ]
        headers = {
        'Host': 'goodevent.tdc.mi.th',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'DNT': '1',
        'Accept': '*/*',
        'Origin': 'https://goodevent.tdc.mi.th',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://goodevent.tdc.mi.th/event/create',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Authorization': 'Bearer'+' '+Token
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # print(response.text)

        imgURL = response.json()[0]['fileUrl']
        print('uploaded image')




        # create goodEvent

        url = "https://goodevent.tdc.mi.th/api/v1/event"

        payload = json.dumps({
        "doDateTime": datestr,
        "endDateTime": datestr,
        "typeEvent": {
            "id": eventTypeID,
            "name": Name,
            "description": Description
        },
        "nameEvent": ชื่อเรื่อง,
        "location": สถานที่,
        "imagePath": [
            imgURL
        ],
        "socialMedia": [
            "",
            "",
            ""
        ],
        "eventDetail": รายละเอียด,
        "citizenId": Username[i],
        "approvalStatus": "waiting",
        "unitTrainingId": "1"
        })
        headers = {
        'Host': 'goodevent.tdc.mi.th',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'DNT': '1',
        'Accept': '*/*',
        'Origin': 'https://goodevent.tdc.mi.th',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://goodevent.tdc.mi.th/event/create',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer'+' '+Token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        print('created goodEvent for '+Username[i])

main()
