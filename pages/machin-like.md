--
title: Machin-like formulae
--

[Machin's formula (M000000001)](/M000000001) is a formula for &pi; that was discovered by John Machin in 1706:
$$\pi=16\arctan\left(\frac15\right)-4\arctan\left(\frac1{239}\right)$$
There are a huge number of Machin-like formulae that have since been discovered, all of which
are of the form:
$$\pi=a_0\arctan(b_0)+a_1\arctan(b_1)+a_2\arctan(b_2)+\dots$$
where the \(a\)s and \(b\)s are rational numbers.

In many sources, Machin-like formulae are written as formulae for computing \(\pi/4\), and so Machin's formula would be written as
$$\frac\pi4=4\arctan\left(\frac15\right)-\arctan\left(\frac1{239}\right).$$
On this website, we follow the convention of the formulae always being equal to \(\pi\).

## Compact notation
On the page for each Machin-like formula, you will find the formula in compact notation.
In this notation, <code>a[b]</code> represents \(a\arctan(1/b)\). For example, the compact formula
<code>16[5] - 4[239]</code> represents [Machin's formula](/M000000001), ie
$$\pi=16\arctan\left(\frac15\right)-4\arctan\left(\frac1{239}\right)$$

## Lehmer's measure
Lehmer's measure as introduced in 1938 <ref author="Lehmer, Derrick Henry" year="1938" title="On Arccotangent Relations for &pi;" journal="American Mathematical Monthly" volume="45" issue="10" pagestart="657" pageend="664" doi="10.2307/2302434">
as a measure of how computationally efficient a Machin-like formula is, with lower values corresponding
to more efficient formulae.

For the general Machin-like formula
$$\pi=a_0\arctan(b_0)+a_1\arctan(b_1)+a_2\arctan(b_2)+\dots$$
Lehmer's measure is computed using
$$\sum_i\frac1{\log_{10}\left(\frac1{b_1}\right)}.$$
For example, for [Machin's formula](/M000000001), Lehmer's measure is
$$\frac1{\log_{10}(5)}+\frac1{\log_{10}(239)}=1.85112$$
