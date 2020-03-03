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
    S_1 \\
    S_2 \\
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
\frac{\partial S_n(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}
 = w_n e^{i(\psi t_n + \phi)}
\left[\begin{array}{c}
        1\\
        \omega\\
        i\left(W + \omega F \right)  \\
        it_n\left(W + \omega F \right)  \\
\end{array}\right]
\end{align*}
$$

The Slepian-Bangs formula provides an analytical expression for the Fisher information matrix, $\mathbf{\mathcal{F}}$, assuming a complex Gaussian noise distribution [1, 2]:

$$
\begin{align*}
    \mathbf{\mathcal{F}} 
    =
    \frac{2}{\sigma^{2}}
    \sum_{n=1}^{2} 
        \left( w_n^2 \textrm{Re}
            \left\{
                \left(\frac{\partial S_n(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}\right)
                \left(\frac{\partial S_n(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}\right)^{H}
            \right\}
        \right) 
    \label{eq:FIM}
\end{align*}
$$

-----
[1] *Slepian, D.* **Estimation of signal parameters in the presence of noise.** Transactions of the IRE Professional Group on Information Theory 3, 68–89 (1954)

[2] *Besson, O. & Abramovich, Y. I.* **On the Fisher Information Matrix for Multivariate Elliptically Contoured Distributions.** IEEE Signal Process. Lett. 20, 1130–1133 (2013)

-----
> **[{{ site.author.name }}](https://staff.ki.se/people/henrry)**  
> {{ site.author.institute }}
>
{{ site.author.email }}