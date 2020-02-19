---
layout: page
title: Optimization of Gradient Waveforms
description: Henric Rydén
---
{% include mathjax.html %}

Below is an interactive figures showing the search space of the dBW-RARE sequence for varying t_a.
Hovering the top plots will render the associated gradients and dephasing of fat.
The top right subplot shows the NSA where only dephasing times are taken into account and not the differing bandwidths, where several equally conditioned options are available if the available acquisition time is sufficiently long.
The difference between the top left and right plot gives an indication of the NSA loss attributed to dual bandwidths.

Try setting the available acquisition time to 6 ms and find where in/opposed phase occurs.
It does not achieve optimal sampling!

The figure might take some time to load.

<iframe src="../assets/plots/coupledGradients.html"
    sandbox="allow-same-origin allow-scripts"
    width="110%"
    height="810"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

> **{{ site.author.name }}**
>
{{ site.author.email }}
