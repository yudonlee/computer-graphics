# Bvh Viewer

# 실행 환경

Python 3.9.3  
numpy  
glfw

# 기능설명

# 1. Bvh file load and render it using T-pose skeleton

- bvh file을 실행 윈도우에 drag할 때, drop_callback()으로 파일을 받아와서 필요 정보들을 파싱하여 전역변수에 저장한다.

- 파일 단순 로드시 t-pose형태의 line-segment를 연결한 skeleton이 나오게 된다.

- static mode일 땐, glPushMatrix()와 glPopMatrix()를 사용하는 대신, parent-offset에 current offset을 더해주어 line-segment를 stack의 형태로 그리게 된다.
  (ex. 팔의 상대좌표 = 몸통의 절대좌표 + 팔의 절대좌표)

- Animating mode일 땐 glPushMatrix()와 glPopMatrix()를 통해 glRotate와 glTranslatef를 사용하여 offset 위치를 계산하였다.

<img width="80%" src="https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment3/Image/t-shape.png"/>

# 2. Animating hierarchical model rendering

key 'space bar'를 누를 시, animating mode가 활성화 된다.

- bvh file의 정보들을 파싱하여 저장한 전역변수 rotations에서 움직임의 정보들을 불러와서 물체를 동작시킨다.

- 이때 시간당 읽게되는 line(bvh file에서 motion에 해당하는 Lines)들을 조절하여 프레임을 조절한다.

- 이때 움직이는 물체를, line segment가 아닌 cube로 그리게 될 경우, local frame의 원점에서 현재의 offset을 이어주는 vector위에 큐브를 그려야한다.(회전축을 의미하며 또다른 말로는 eigenvector라고 한다.)

- 해당 축을 기준으로 x, y, z축을 rotation 시켜서 렌더링 해야한다.

# 3. rendering 결과

<img width="80%" src="https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment3/Image/bvh_animation.gif"/>
