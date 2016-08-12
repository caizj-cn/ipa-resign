

help:
http://www.runoob.com/python/python-dictionary.html


view-source:http://www.hotniao.com/download/download2.aspx?id=63



ipa重签名流程
unzip zhixin.ipa

rm -rf Payload/Landlord-mobile.app/_CodeSignature

cp embedded.mobileprovision Payload/Landlord-mobile.app/embedded.mobileprovision

/usr/bin/codesign -f -s "iPhone Distribution: Beijing TianRuiDiAn Network Technology Co,Ltd." --entitlements Entitlements.plist Payload/Landlord-mobile.app

zip -r test.ipa Payload
