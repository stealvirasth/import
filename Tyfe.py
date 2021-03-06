# -*- coding: utf-8 -*-

from linepy import *
from akad import *
import traceback
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, urllib, urllib,pickle
from datetime import datetime
from random import randint

print("""

\033["""+str(randint(0,1))+""";"""+str(randint(31,36))+"""mplay free\nBy Nack Migicavi\033[0m

""")

with open('tval.pkl', 'rb') as f:
    [linepytoken,wait] = pickle.load(f,encoding='latin1')

if len(sys.argv) == 2 and sys.argv[1] == "reset":
    cltoken = ""
    with open('tval.pkl', 'wb') as f:
        pickle.dump([linepytoken,wait], f)
    os._exit(0)

if linepytoken == "":
    linepy = LINE()
    linepytoken = linepy.authToken
else:
    try:
        linepy = LINE(linepytoken)
    except KeyboardInterrupt as e:
        raise e
    except:
        linepy = LINE()
        linepytoken = linepy.authToken

print("authToken: %s" % (linepytoken))


user1 = linepy.profile.mid
admin = OEPoll(linepy)

start_runtime = datetime.now()

wait = {
    'alwayread':False,
    'autoBlock':False,
    'welcomepic':False,
    'welcomemessage':False,
    'autoadd':False,
    'messageadd':"",
    'autotag':False,
    'tagmessage':"",
}

userhelp = """คำสั่งทั้งหมด (พิมพ์ ! ตามด้วยคำสั่ง):

-help
-myid
-me
-myname
-speed
-name
-kick (@)
-uid (@)
-danyall [text]
-mentionall
-sh *
-invitetocall
-uptime
-remember [1:2]
-forget [1]
-forgetall
-autodeny off
-autodeny [numbers]
-autoread on/off
-autoblock on/off
-welcomemessage on/off
-welcomemessage:[text]
-setmessageadd:[text]
-autoadd on/off

**คำสั่งสำหรับบัญชีนี้เท่านั้น**"""

procLock = 0
mentmedat = {}
respRemember = {}

def user1scipt(op):
    global startruntime
    global user1
    global wait
    global alwayread
    global autoBlock
    global welcomepic
    global welcomemessage
    global autoadd
    global messageadd
    global autotag
    global tagmessage
    global autoDeny
    global procLock
    global mentmedat
    global respRemember
    try:
        if op.type == 0:
            return

        if op.type == 5:
            if wait['autoBlock'] == True:
                linepy.blockContact(op.param1)

            if wait['autoadd'] == True:
                linepy.findAndAddContactsByMid(op.param1)
                if (wait["messageadd"] in [""," ","\n",None]):
                    pass
                else:
                    linepy.sendMessage(op.param1,str(wait["messageadd"]))

        if op.type ==13:
            invitor = op.param2
            gotinvite = []
            if "\x1e" in op.param3:
                gotinvite = op.param3.split("\x1e")
            else:
                gotinvite.append(op.param3)
            if invitor in user1 in gotinvite:
                linepy.acceptGroupInvitation(op.param1)
            else:
                group = linepy.getGroup(op.param1)
                if len(group.members) <= autoDeny:
                    procLock += 1
                    linepy.acceptGroupInvitation(op.param1)
                    linepy.leaveGroup(op.param1)

        if op.type == 17:
            if wait['welcomemessage'] and "welcomemessage" in wait:
               cnt = cl.getContact(op.param2)
               linepy.sendMessage(op.param1,cnt.displayName + "\n" + str(wait["welcomemessage"]))

            if wait['welcomepic'] and "welcomepic" in wait:
                cnt = cl.getContact(op.param2)
                linepy.sendImageWithURL(op.param1,"http://dl.profile.line.naver.jp/" + cnt.pictureStatus)

        if op.type == 26:
             msg = op.message
             msg.from_ = msg._from
             if msg.contentMetadata != {}:
                 try:
                     prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                     tagme = False
                     alluids = []
                     for i in range(len(prov)):
                         alluids.append(prov[i]["M"])
                         if prov[i]["M"] == mid:
                             tagme = True
                     alluids = list(set(alluids))
                     if tagme:
                        if len(alluids) <= 4:
                            if msg.to not in mentmedat:
                                mentmedat[msg.to] = []
                                tagfrom = msg.from_
                                tagtime = nowS = datetime.strftime(datetime.now(),"%H:%M:%S")
                                tagid = msg.id
                                mentmedat[msg.to].append(
                                    {
                                        "tfrom" : tagfrom,
                                        "ttime" : tagtime,
                                        "tid" : tagid
                                    }
                                )
                 except:
                     pass

             if wait["alwayread"]:
                 linepy.sendChatChecked(msg.from_,msg.id)
             else:
                 linepy.sendChatChecked(msg.to,msg.id)

             if msg.to in respRemember and msg.text in respRemember[msg.to]:
                 if msg.toType != 0:
                     linepy.sendMessage(msg.to,respRemember[msg.to][msg.text])
                 else:
                     linepy.sendMessage(msg.from_,respRemember[msg.to][msg.text])

             if wait["tagmessage"] == True:
                 linepy.sendMessage(op.param1)
                 if (wait["tagmessage"] in [""," ","\n",None]):
                     pass
                 else:
                     linepy.sendMessage(op.param1,str(wait["tagmessage"]))

        if op.type == 25:
            msg = op.message
            if msg.text is None:
               return

            elif msg.text.lower() == "!help":
                linepy.sendMessage(msg.to,userhelp)

            elif msg.text.lower() == "!myid":
                linepy.sendMessage(msg.to,user1)

            elif msg.text.lower() == "!me":
                back = user1
                linepy.sendContact(msg.to,beach)

            elif msg.text.lower() == "!myname":
                G = linepy.getContact(user1)
                linepy.sendMessage(msg.to,G.displayName)

            elif msg.text.lower() == "!speed":
                start = time.time()
                linepy.sendMessage(msg.to,"กำลังทดสอบ(｀・ω・´)")
                linepy.sendMessage(msg.to,str(int(round((time.time() - start) * 1000)))+" ms")

            elif "!name " in msg.text.lower():
                spl = re.split("!name ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prof = linepy.getProfile()
                    prof.displayName = spl[1]
                    linepy.updateProfile(prof)
                    linepy.sendMessage(msg.to,"เปลี่ยนชื่อสำเร็จแล้ว(｀・ω・´)")

            elif "!kick" in msg.text.lower():
                if msg.contentMetadata is not None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            linepy.kickoutFromGroup(msg.to,[target])
                        except:
                            linepy.kickoutFromGroup(msg.to,[target])
                    else:
                        pass

            elif "!uid " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('!uid '),re.IGNORECASE)
                    namel = red.sub('',msg.text)
                    namel = namel.lstrip()
                    namel = namel.replace(" @","$spliter$")
                    namel = namel.replace("@","")
                    namel = namel.rstrip()
                    namel = namel.split("$spliter$")
                    gmem = linepy.getGroup(msg.to).members
                    for targ in gmem:
                        if targ.displayName in namel:
                            linepy.sendMessage(msg.to,targ.displayName+": "+targ.mid)

            elif "!denyall" in msg.text.lower():
                 spl = re.split("!denyall",msg.text,flags=re.IGNORECASE)
                 if spl[0] == "":
                     spl[1] = spl[1].strip()
                     ag = linepy.getGroupIdsInvited()
                     txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+"กลุ่ม"
                     if spl[1] != "":
                         txt = txt + " ด้วยข้อความ \""+spl[1]+"\""
                     txt = txt + "\nกรุณารอสักครู่.."
                     linepy.sendMessage(msg.to,txt)
                     procLock = len(ag)
                     for gr in ag:
                         try:
                             linepy.acceptGroupInvitation(gr)
                             if spl[1] != "":
                                 linepy.sendMessage(gr,spl[1])
                             linepy.leaveGroup(gr)
                         except:
                             pass
                     linepy.sendMessage(msg.to,"สำเร็จแล้ว(｀・ω・´)")

            elif "!setmessageadd:" in msg.text.lower():
                wait['messageadd'] = msg.text.replace("!setmessageadd:","")
                linepy.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif "!tagmessage:" in msg.text.lower():
                wait['tagmessage'] = msg.text.replace("!tagmessage:","")
                linepy.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif msg.text.lower().startswith("!mentionall"):
                data = msg.text[len("!mentionall"):].strip()
                if data == "":
                    group = linepy.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    strt = len(str(count)) + 2
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        akh = akh + len(str(count)) + 2 + 5
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                linepy.sendMessage(msg)
                            except:
                                linepy.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                       linepy.sendMessage(msg.to, text=cb2,contentMetadata={u'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'},contentType=0)
                    except:
                       linepy.sendMessage(msg.to,"[[NO MENTION]]")

            elif msg.text.lower() == "!checkmention":
                if msg.to in mentmedat and mentmedat[msg.to] != []:
                    text = ""
                    for data in mentmedat[msg.to]:
                        print("555")
                        try:
                            conname = cl.getContact(data["tfrom"]).displayName
                        except:
                            conname = "[DELETED]"
                        text += "[%s] %s\nline://nv/chatMsg?chatId=%s&messageId=%s\n\n" % (data["ttime"],conname,msg.to,data["tid"])
                    text = text[:-2]
                    try:
                        linepy.sendMessage(msg.to,text)
                    except Exception as e:
                        linepy.sendMessage(msg.to,str(e))
                    del mentmedat[msg.to]
                else:
                    linepy.sendMessage(msg.to,"ไม่มีการกล่าวถึงก่อนหน้านี้(｀・ω・´)")

            elif msg.text.lower() == "!resetmention":
                dkey = mentmedat.pop(msg.to,None)
                linepy.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงเรียบร้อยแล้ว")


            elif msg.text.lower() == "!resetallmention":
                mentmedat = {}
                linepy.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงทั้งหมดแล้ว")

            elif "!sh " in msg.text.lower():
                spl = re.split("!sh ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    try:
                        linepy.sendMessage(msg.to,subprocess.getoutput(spl[1]))
                    except:
                        pass

            elif msg.text.lower() == "!invitetocall":
                exc = linepy.getGroup(msg.to).members
                zxc = linepy.getProfile().mid
                linepy.inviteIntoGroupCall(msg.to,[uid.mid for uid in exc if uid.mid != zxc])
                linepy.sendMessage(msg.to,"เชิญเข้าร่วมการคอลเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!uptime":
                linepy.sendMessage(msg.to,str(datetime.now() - start_runtime)[:-7].split(":")[0]+" hour, "+str(datetime.now() - start_runtime)[:-7].split(":")[1]+" minute, "+str(datetime.now() - start_runtime)[:-7].split(":")[2]+" second,")

            elif msg.text.lower().startswith("!remember "):
                data = msg.text[len("!remember "):]
                keyword = data.split(":",1)[0]
                if keyword.lower().startswith("!remember") or keyword.lower().startswith("!forget") or keyword in ["",None]:
                    raise ValueError
                response = data.split(":",1)[1]
                if response in ["",None]:
                    raise ValueError
                if msg.to not in respRemember:
                    respRemember[msg.to] = {}
                respRemember[msg.to][keyword] = response
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    linepy.sendMessage(msg.to,"จำแล้ว (｀・ω・´)"+tm)
                else:
                    linepy.sendMessage(msg._from,"จำแล้ว (｀・ω・´)"+tm)

            elif msg.text.lower().startswith("!forget "):
                keyword = msg.text[len("!forget "):]
                if keyword in ["",None]:
                    raise ValueError
                if msg.to in respRemember and keyword in respRemember[msg.to]:
                    dkey = respRemember[msg.to].pop(keyword,None)
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        linepy.sendMessage(msg.to,"ลืมแล้ว (｀・ω・´)"+tm)
                    else:
                        linepy.sendMessage(msg._from,"ลืมแล้ว (｀・ω・´)"+tm)
                else:
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        linepy.sendMessage(msg.to,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
                    else:
                        linepy.sendMessage(msg._from,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "!forgetall":
                dkey = respRemember.pop(msg.to,None)
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    linepy.sendMessage(msg.to,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)
                else:
                    linepy.sendMessage(msg.from_,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)

            elif "!welcomemessage:" in msg.text.lower():
                 c = msg.text.replace("!welcomemessage:","")
                 if c in [""," ","\n",None]:
                     linepy.sendMessage(msg.to,"เกิดข้อผิดพลาด!!(｀・ω・´)")
                 else:
                     wait['welcomemessage'] = c
                     linepy.sendMessage(msg.to,"ตั้งค่าข้อความสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower() == "!autodeny off":
                autoDeny = -1
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower().startswith("!autodeny "):
               try:
                   autoDeny = int(msg.text[len(".autodeny "):])
                   linepy.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")
               except:
                   linepy.sendMessage(msg.to,"พบข้อผิดพลาด(｀・ω・´)")

            elif msg.text.lower() == "!autoread on":
                if wait["alwayread"] == True:
                    linepy.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = False
                else:
                    if wait["alwayread"] == False:
                        linepy.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "!autoread off":
                if wait["alwayread"] == False:
                    linepy.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = True
                else:
                    if wait["alwayread"] == True:
                        linepy.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "!autoblock on":
                if wait['autoBlock'] == True:
                    linepy.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = False
                else:
                    if wait['autoBlock'] == False:
                        linepy.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "!autoblock off":
                if wait['autoBlock'] == False:
                    linepy.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = True
                else:
                    if wait['autoBlock'] == True:
                        linepy.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "!welcomepic on":
                if wait['welcomepic'] == False:
                    linepy.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = True
                else:
                    if wait['welcomepic'] == True:
                        linepy.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!welcomepic off":
                if wait['welcomepic'] == True:
                    linepy.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = False
                else:
                    if wait['welcomepic'] == False:
                        linepy.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!welcomemessage on":
                if wait['welcomemessage'] == False:
                    linepy.sendMessage(msg.to,"เปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")
                    wait['welcomemessage'] = True
                else:
                    if wait['welcomemessage'] == True:
                        linepy.sendMessage(msg.to,"เปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!welcomemessage off":
                if wait['welcomemessage'] == True:
                    linepy.sendMessage(msg.to,"ปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")
                    wait['welcomemessage'] = False
                else:
                    if wait['welcomemessage'] == False:
                        linepy.sendMessage(msg.to,"ปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!autoadd on":
                if wait['autoadd'] == False:
                    cl.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")
                    wait['autoadd'] = True
                else:
                    if wait['autoadd'] == True:
                        linepy.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")

            elif msg.text.lower() == "!autoadd off":
                if wait['autoadd'] == True:
                    linepy.sendMessage(msg.to,"ปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")
                    wait['auto'] = False
                else:
                    if wait['autoadd'] == False:
                        linepy.sendMessage(msg.text,"ปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")

            elif msg.text.lower() == "!autotag on":
                if wait['autotag'] == False:
                    linepy.sendMessage(msg.to,"เปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
                    wait['autotag'] = True
                else:
                    if wait['autotag'] == True:
                        linepy.sendMessage(msg.to,"เปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "!autotag off":
                if wait['autotag'] == True:
                    linepy.sendMessage(msg.to,"ปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
                    wait['autotag'] = False
                else:
                    if wait['autotag'] == False:
                        linepy.sendMessage(msg.to,"ปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
    except:
        traceback.print_exc()

try:
    while True:
        ops = admin.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                user1scipt(op)
                admin.setRevision(op.revision)
except:
    traceback.print_exc()
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,wait], f)
