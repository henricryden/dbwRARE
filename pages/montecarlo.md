---
layout: page
mathjax: true
title: Monte Carlo Simulations
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
    + 
    \underbrace{
        \left[
        \begin{matrix}
        \epsilon_1 \\
        \epsilon_2 \\
        \end{matrix}
        \right]
    }_\mathbf{\mathcal{E}}
\end{align*}
$$

The forward model $\mathbf{B \Lambda A X}$ was applied once and 1000 samples were generated for each dephasing time pair $(t_1, t_2)$ by adding complex noise, $\mathbf{\mathcal{E}}$.
Independent noise was added to the real and imaginary channel, drawn from a normal distribution of zero mean and standard deviation $\sigma = 0.01$.

Field map was estimated by minimizing the cost function $J$ (as described in [3]) for 50 $\psi$ candidates, placed on a 1 Hz raster with the center point around the ground truth of 40 Hz:


$$
\begin{align*}
  J({\psi}) = \left \|\mathbf{S}  e^{-i\phi}
  -
  \mathbf{B}(\psi)
  \mathbf{L}
  \textrm{Re}(\mathbf{L}^-
  \mathbf{B}(\psi)^H
  \mathbf{S}
  e^{-i\phi}
  )
  \right \|_2,
\end{align*}
$$


where $\mathbf{L} =  \mathbf{\Lambda A}$.
The initial phase $\phi$ was calculated for each field map candidate $\psi$ as follows:

$$
\begin{align*}
  \phi
  =
  \frac{1}{2}
  \angle
  \left(
    \mathbf{L}^H
    \mathbf{B}(\psi)^H
    \mathbf{S}
  \right)^T
  \textrm{Re}\left(
    \mathbf{L}^H\mathbf{L}
  \right)^{-1}
  \left(
    \mathbf{L}^H
    \mathbf{B}(\psi)^H
    \mathbf{S}
  \right)
\label{eq:initialPhase}
\end{align*}
$$

Given the estimated off-resonance $\hat{\psi}$ and $\hat{\phi}$ for each sample, *real-valued* estimates of $\mathbf{X}$ were calculated according to [4]:

$$
\begin{align*}
  \mathbf{\hat{X}} = 
  \left[
    \begin{matrix}
    \mathbf{L} \\
    \mathbf{L}^* \\
    \end{matrix}
  \right]^+
  \left[
    \begin{matrix}
    \mathbf{SB}            (\hat{\psi})  e^{-i \phi} \\
    \left(\mathbf{SB}            (\hat{\psi})  e^{-i \phi} \right)^* \\
    \end{matrix}
  \right]
    
\end{align*}
$$

Where the + and * superscript denotes the pseudoinverse and conjugate operator, respectively.
The NSA of the species is calculated from the signal variance divided by the variance of the estimate $s \in \left\\{ W, F \right\\} $ of interest:

$$
\begin{align*}
\textrm{NSA}_{\hat{s}}
=
\frac{
  \sigma ^2
}{
  \textrm{Var}\left(
    \hat{s}
    \right)
}

\end{align*}
$$



---

### Equal Weights
Below is a Monte Carlo simulation of the equally weighted two-point fat water inverse problem, with axes corresponding to dephasing times.
Instead of showing the nominal times, the dephasing angle is used instead to avoid the field strength dependency.
At 1.5 / 3 T, $\pi$ corresponds to 1.15 / 2.30 ms.

The results shown below is essentially a reproduction of the results by [1] and [2], with the echo weights $w_1 = w_2 = \frac{1}{\sqrt{2}}$:

<iframe src="../assets/plots/unweighted.html"
    sandbox="allow-same-origin allow-scripts"
    width="120%"
    height="410"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

The above figure shows the previously established well-conditioned sampling of where one echo is acquired in-phase while the other is an opposed-phase echo.

-----

### Weighted Case
Since the variance increases quadratically with a linear scaling factor, i.e. $\textrm{Var}(aX) = a^2 \textrm{Var(X)}$, weights must be chosen to achieve unit variance in its combined case:
$w_1^2 + w_2^2 = 1$.
We can express the weights from the first-echo fraction $f = \frac{w_1}{w_1 + w_2} \in [0,1]$:

$$
\begin{align*}
        w_1 = \frac{f}  {\sqrt{\left(1-f\right)^2 + f^2}} \\
        w_2 = \frac{1-f}{\sqrt{\left(1-f\right)^2 + f^2}}
        \label{eq:weights}
\end{align*}
$$

Below is a plot of $w_1$ and $w_2$ as a function of f:

<iframe src="../assets/plots/weights.html"
    sandbox="allow-same-origin allow-scripts"
    width="100%"
    height="200"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

Setting $t_1 = 0$, we can investigate the effective NSA of water and fat with varying $f$, $t_2$ and fat fraction, shown below:


<iframe src="../assets/plots/weighted.html"
    sandbox="allow-same-origin allow-scripts"
    width="120%"
    height="410"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>



Python and MATLAB code for the simulations is available at the [Github repository](https://github.com/henricryden/dbwRARE)

-----
[1] *Eggers, H. & Börnert, P.* **Chemical shift encoding-based water-fat separation methods.**
J. Magn. Reson. Imaging 40, 251–268 (2014).

[2] *Berglund, J., et al.* **Two-point dixon method with flexible echo times.**
Magn. Reson. Med. 65, 994–1004 (2011).

[3] *Rydén, H., et al.* **T1 weighted fat/water separated PROPELLER acquired with dual bandwidths.**
Magn. Reson. Med. 80, 2501–2513 (2018).

[4] *Berglund, J. et al.* **Fat/water separation in k-space with real-valued estimates and its combination with POCS.**
Magn. Reson. Med. (2019). doi:10.1002/mrm.27949