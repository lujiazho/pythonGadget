用平面坐标系上的点![formula](https://render.githubusercontent.com/render/math?math=(x_i,y_i))描述个体，假设任意健康个体![formula](https://render.githubusercontent.com/render/math?math=A_i(x_i,y_i))和病毒携带个体![formula](https://render.githubusercontent.com/render/math?math=B_j(x_j,y_j))之间的距离为![formula](https://render.githubusercontent.com/render/math?math=d_{ij})，病毒携带者![formula](https://render.githubusercontent.com/render/math?math=B_j)向![formula](https://render.githubusercontent.com/render/math?math=A_i)传播病毒并使![formula](https://render.githubusercontent.com/render/math?math=B_j)向![formula](https://render.githubusercontent.com/render/math?math=A_i)感染的几率为![formula](https://render.githubusercontent.com/render/math?math=p_{ij})，二者的关系用式![formula](https://render.githubusercontent.com/render/math?math=\eqref{eq1})描述

$$
p_{ij}(d_{ij})=
\begin{cases}
(1+w_{ij})p0_{i}  &\text{if }d_{ij} \leq d0_{i}\\
(1+w_{ij})p0_{i}α_{i}^{-(d_{ij}-d0_{i})} &\text{if }d_{ij} > d0_{i}
\end{cases}
\tag{1}\label{eq1}
$$

其中，

> $d0_{i}$为个体$A_i(x_i,y_i)$的临界距离；（反映个体自身的抵抗能力）
> $w_{ij}$反映个体$A_i$和$B_j$的亲密度，其值取0~1，其值越大，越容易感染；
> $p0_{i}$为$w_{ij}=0$时$A_i$在临界距离$d_{0i}$内被感染的几率，也称基础感染率；（反映个体自身的抵抗能力）
> $α_i$为大于1的系数，反映在临界距离外，个体被感染几率的衰减程度，越大，衰减越快；

需要注意的是，此处所指的距离是广义距离，并不是指现实中两个个体的实际距离，可以认为是两个体多方面的综合距离，包括个体之间的时空关系、亲密度关系、抵抗能力等，同时$p_{ij} (d_{ij})≠p_{ji} (d_{ij})$，因为$d_{ij}$不是唯一影响感染率的变量。



## 已添加模块

1、增加指定特定个体隔离操作



2、增加传染性参数

现基于原作者，增加参数：病毒携带者$B_j$的传染性$p1_j$，其范围在0~1之间，从而得到如下公式$\eqref{eq3}$
$$
p_{ij}(d_{ij},w_{ij},d0_{i},p0_{i},p1_j,α_i)=
\begin{cases}
\frac{(1+w_{ij})p0_{i}}{p1_j}  &\text{if }d_{ij} \leq d0_{i}\\
\frac{(1+w_{ij})p0_{i}}{p1_j}α_{i}^{-(d_{ij}-d0_{i})} &\text{if }d_{ij} > d0_{i}
\end{cases}
\tag{2}\label{eq3}
$$
3、增加多个感染源



4、增加随机传染性



5、根据传染性可视化病毒携带者大小





## 待添加模块

1、随机隔离模块



2、指定特定个体步长



3、随机步长设置



4、患者自然恢复模块



5、疫苗增加抵抗力模块

（减少基础感染率或者临界距离，或增大α阿尔法）

6、限制通行，减少人流量

（减少移动步长，可以不同时间限制不同人群）

7、控制感染源

（受控感染源恢复快，且无法移动；如 可对所有感染源找中心，并使其往中心靠）
