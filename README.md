2017-01-01

增加了对python3的支持（原作者为python2版本）

-----------------------------------------

import DiscuzAPI

robot = DiscuzAPI(sys.argv[1], sys.argv[2], sys.argv[3])

robot.login()

robot.sign()

robot.speak()

robot.publish(21,"test",imgId)

robot.reply(10)

imageData = open('test.jpg', 'rb').read()

print robot.uploadImage( imageData )

