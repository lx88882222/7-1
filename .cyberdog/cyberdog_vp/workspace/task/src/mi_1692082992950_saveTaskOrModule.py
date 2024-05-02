# Copyright (c) 2023 Beijing Xiaomi Mobile Software Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time
import threading
import mi.cyberdog_vp.decorator
from mi.cyberdog_bringup.manual import get_namespace
from mi.cyberdog_vp.utils import get_argv
from mi.cyberdog_vp.abilityset import Cyberdog
sys.path.append(os.path.join('/home/mi/.cyberdog/cyberdog_vp/workspace', 'module', 'src'))

now_task_id, now_task_parameters = get_argv()
task_id = now_task_id if len(now_task_id) != 0 else 'mi_1692082992950_saveTaskOrModule'
task_parameters = now_task_parameters if len(now_task_parameters) != 0 else ''

print(time.strftime("任务开始时间为：%Y年%m月%d日 %H点%M分%S秒", time.localtime()))
print("任务线程标识符：%d" % threading.get_ident())
print("当前装饰器版本：%s" % mi.cyberdog_vp.decorator.version())
cyberdog = Cyberdog(task_id, get_namespace(), True, task_parameters)
cyberdog.set_log(False)
cyberdog.task.start()
cyberdog.task.block('RBpqO=zS:Min@~s1YZVV')
cyberdog.task.block('weRt~_]Pq4$:(8r/z~W|')
cyberdog.audio.play('任务开始',50);
cyberdog.task.block('wBuJFjbixTZDStbv,PIi')
while True: 
    cyberdog.task.block('M2S3v;kdaZ`r~Ox55ZF9')
    if cyberdog.gesture.recognized(60, 1).data.pushing_hand_or_two_fingers_away:
        cyberdog.task.block('f5gqTX5Dv3FyFZ7fnukR')
        cyberdog.motion.go_straight(-0.3,0,3);
    cyberdog.task.block('V%z(3VN}LUjlW!{51~l.')
    if cyberdog.gesture.recognized(60, 1).data.sliding_hand_or_two_fingers_up:
        cyberdog.task.block('kLxd`W2DMMgcixG%pdv^')
        cyberdog.motion.go_straight(0.3,0,3);
    cyberdog.task.block('%{.,?)}/C2(BI`46YQ)-')
    if cyberdog.gesture.recognized(60, 1).data.sliding_hand_or_two_fingers_right:
        cyberdog.task.block('64!qdB06Fw~K5;46`rk/')
        cyberdog.motion.lateral_movement(0.3,0,2);
    cyberdog.task.block('aRp]h5it5_%mwP-51S]]')
    if cyberdog.gesture.recognized(60, 1).data.sliding_hand_or_two_fingers_left:
        cyberdog.task.block('GDF5G_f;%KPU0[DmJ@qy')
        cyberdog.motion.lateral_movement(-0.3,0,2);
    cyberdog.task.block('_)?}y(^UC+tyuy?um;.y')
    if cyberdog.gesture.recognized(60, 1).data.thumb_up:
        cyberdog.task.block('CIYR1A-r#/{;uvQ}h_+=')
        cyberdog.motion.bow();
        cyberdog.task.block('UBsLr?%w3mp.fi`d#bI`')
        cyberdog.motion.resume_standing();


cyberdog.task.stop()
cyberdog.shutdown()

