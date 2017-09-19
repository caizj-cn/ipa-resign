

help:
http://www.runoob.com/python/python-dictionary.html



ipa重签名流程
unzip zhixin.ipa

rm -rf Payload/Landlord-mobile.app/_CodeSignature

cp embedded.mobileprovision Payload/Landlord-mobile.app/embedded.mobileprovision

/usr/bin/codesign -f -s "iPhone Distribution: Beijing TianRuiDiAn Network Technology Co,Ltd." --entitlements Entitlements.plist Payload/Landlord-mobile.app

zip -r test.ipa Payload

参考说明：
1.http://www.jianshu.com/p/15edfe11f8ac
2.http://www.jianshu.com/p/bdbac933c1be
