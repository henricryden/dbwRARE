---
layout: page
mathjax: true
title: Cramér Rao Bounds
description: Henric Rydén
---
{% include mathjax.html %}

The two-point signal model used for the simulations is shown below:

$$
\begin{align*}
\underbrace{
    \left[
    \begin{matrix}
    S(t_1) \\
    S(t_2) \\
    \end{matrix}
    \right]
    }_{\mathbf{S}}
    =
    e^{i\phi}
    \underbrace{
    \left[
    \begin{matrix}
    e^{i\psi t_1} & 0 \\
    0 & e^{i\psi t_2} \\
    \end{matrix}
    \right]
    }_{\mathbf{B}(\psi)}
    \underbrace{
    \left[
    \begin{matrix}
    w_1 & 0 \\
    0 & w_2 \\
    \end{matrix}
    \right]
    }_{\mathbf{\Lambda}}
    \underbrace{
    \left[
    \begin{matrix}
    1 & e^{i\omega t_1} \\
    1 & e^{i\omega t_2} \\
    \end{matrix}
    \right]
    }_{\mathbf{A}}
    \underbrace{
    \left[
    \begin{matrix}
    W \\
    F \\
    \end{matrix}
    \right]
    }_{\mathbf{x}}
\end{align*}
$$

The signal from echo $n$ can be derived with respect to the real-valued model parameter vector $\boldsymbol{\theta} = \left[\begin{array}{cccc} W & F & \phi & \psi \end{array} \right]^T$:

$$
\begin{align*}
\frac{\partial y_n(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}
 = w_n e^{i(\psi t_n + \phi)}
\left[\begin{array}{c}
        1\\
        a(t_n)\\
        i\left(W + a(t_n) F \right)  \\
        it_n\left(W + a(t_n) F \right)  \\
\end{array}\right]
\end{align*}
$$

-----
> **{{ site.author.name }}**
>
{{ site.author.email }}
