# Basic OpenGL Viewer

Basic OpenGL Viewer를 구현한다.
이때 마우스 버튼의 클릭과, 휠을 작동하여 구면좌표계에서 원점을 중심으로 한 크기가 1인 정사각형을 보게 된다.

# 실행 환경

Python 3.9.3  
numpy  
glfw

# 기능설명

# 1. Orbit(mouse left button + Drag)

마우스 왼쪽 버튼을 누르고 마우스 커서를 이동하면 동작한다.

- azimuth와, elevation 각도를 바꿔서, target point로부터 카메라를 돌려서 볼수 있도록 한다.
- 이를 위해서 gluLookAt의 parameter값을 구면좌표계를 이용하여 구한 값으로 바꿔준다.

|                                            initial State                                             |                                            After Orbit                                             |
| :--------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
| ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/image/initialState.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/image/afterOrbit.png) |

# 2. Panning(mouse right button + Drag)

target point와 camera를 상하좌우로 이동시키는 것이다.

- Eye에서 x축과 y축에 평행하도록 이동시키고, 이때 target point또한 동일한 거리로 이동시켜준다.

|                                            initial State                                             |                                            After Panning                                             |
| :--------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: |
| ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/initialState.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/afterPanning.png) |

# 3. Zooming(mouse scroll wheel up or down)

target point를 기준으로 카메라가 target point에 가깝거나, 멀리가게 된다.
Zoom in | Zoom out
:-------------------------:|:-------------------------:
![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/afterZoomIn.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/afterZoomOut.png)

# 4. projection mode

v키를 입력받게 되면, perspective projection과 orthgonal perspective projection 두가지 모드로 번갈아 변경된다.

- Orthogonal projection는 거리에 따라서 edge들의 크기가 다르게 보이는 perspective projection mode와 달리, 모든 edge들의 크기가 동일하게 나타난다.

|                                        Perspective Projection                                        |                                 Orthogonal perspecrive Projection                                  |
| :--------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
| ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/initialState.png) | ![](https://github.com/yudonlee/computer-graphics/blob/main/ClassAssignment1/Image/orthogonal.png) |
