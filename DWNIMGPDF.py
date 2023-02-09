import datetime
import os
import PIL.Image
import requests
from PIL import Image
from googlesearch import search

dir ='C:/Users/kavya/Desktop/SanskritChapters'
filenamelist=[]

chapter=input('Write Chapter name and number in format[Number-Name] - ')

print('Checking Chapter Name...')

f = ""
for url in search((f" NCERT Solution for Class 10 Sanskrit chapter {chapter} Knowledge Gallery") , stop=3):
    f = url if (url[:72] == "https://knowledgegallery.in/ncert-solution-for-class-10-sanskrit-chapter") else f
wwn = f[73:len(f)-1]
suggestion = wwn.split('-')[0] +"-"+ ('-').join(i.capitalize() for i in wwn.split('-')[1:])

if suggestion == chapter:
    pass
elif suggestion == '7-Sauhardam-Prakrite-Shobha': #Exception
    y = input(f"We Suggest changing chapter name to 7-Souhadra-Prakrite-Shobha ? (y/n) - ")
    if y in ("y yes yup yeah sure").split():
        chapter = '7-Souhadra-Prakrite-Shobha'
        print(f"Chapter name changed to {chapter}...")
else:
    y = input(f"We Suggest changing chapter name to {suggestion} ? (y/n) - ")
    if y in ("y yes yup yeah sure").split():
        chapter = suggestion
        print(f"Chapter name changed to {chapter}...")

m=0
newdir= dir+'/'+chapter+('_').join((('_').join(x for x in (i.split(':'))) for i in str(datetime.datetime.now())[0:-7].split(' ')))
os.mkdir(newdir)

print('Figuring out number of pages and Downloading Images. Please Wait...')

for i in range(1,200):
    try:
        img = newdir+f'/{chapter}-Pg-{i}.png'
        #print(img)
        #print(f'https://knowledgegallery.in/wp-content/uploads/2021/04/Class-10-Sanskrit-Solutions/Chapter-{chapter}/Chapter-{chapter}_Page_{str(i)}')
        r = requests.get(f'https://knowledgegallery.in/wp-content/uploads/2021/04/Class-10-Sanskrit-Solutions/Chapter-{chapter}/Chapter-{chapter}_Page_{str(i)}' , stream=True)
        with open(img,'wb') as f:
            for chunk in r:
                f.write(chunk)
        PIL.Image.open(img)
        filenamelist.append(img)
        m=i
    except Exception:
        os.remove(img)
        if i ==1:
            print('Either >=10 or Incorrect Chapter Name ...')
            for x in range(1, 200):
                try:
                    img = newdir + f'/{chapter}-Pg-{x}.png'
                    # print(img)
                    # print(f'https://knowledgegallery.in/wp-content/uploads/2021/04/Class-10-Sanskrit-Solutions/Chapter-12-Anyoktya/Chapter-{chapter}_Page_{str(i)}')
                    r = requests.get(f'https://knowledgegallery.in/wp-content/uploads/2021/04/Class-10-Sanskrit-Solutions/Chapter-{chapter}/Chapter-{chapter}_Page_{(str(0) +str(x) if x<10 else x )}',stream=True)
                    with open(img, 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                    PIL.Image.open(img)
                    m = x
                    filenamelist.append(img)
                except Exception:
                    os.remove(img)
                    if x == 1 :
                        print('Incorrect Chapter Name')
                        exit()
                    else:
                        break
            break
        else:
            break
print('Number Of Pages - %s'%m)
print(f'Converting into pdf - {newdir}/{chapter}.pdf...')

finallist=[]
for x in filenamelist:
    image = Image.open(x)
    im = image.convert('RGB')
    finallist.append(im)

finallist[0].save(f'{newdir}/{chapter}.pdf',save_all=True,append_images = finallist[1:m])
print("All Done!!!")