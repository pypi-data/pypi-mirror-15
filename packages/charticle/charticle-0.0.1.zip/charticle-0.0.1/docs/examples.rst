Examples
--------

Example usages of charticle.

Venn3
^^^^^

Three-circle Venn diagrams are supported, *pace* Drew Conway's
data science (last in this section).

.. plot::
   :context:
   :include-source: true

   >>> import matplotlib
   >>> matplotlib.use('Agg')
   >>> from matplotlib import pyplot as plt
   >>> from charticle.venn import Venn3
   >>> v3 = Venn3(a_name="useful", b_name = "structured", c_name="delimited")
   >>> v3.abc = "discipline"
   >>> v3.title = "Knowledge"
   >>> v3.fontsizes.title = 22
   >>> v3  #doctest: +ELLIPSIS
   Venn3(a_name='useful', b_name='structured', c_name='delimited', ...))
   >>> _ = v3.plot()
   >>> plt.show()


Further can set region sizes:

.. plot::
   :context: close-figs
   :include-source: true

   >>> v3.sizes
   Venn3.Sizes(a=1.0, b=1.0, c=1.0, ab=1.0, ac=1.0, bc=1.0, abc=1.0, normalize=1.0)
   >>> v3.sizes.set_single_weight(1.0) # moot
   Venn3.Sizes(a=1.0, b=1.0, c=1.0, ab=1.0, ac=1.0, bc=1.0, abc=1.0, normalize=1.0)
   >>> v3.sizes.a *= 5
   >>> v3.sizes.set_double_weight(2.0)
   Venn3.Sizes(a=5.0, b=1.0, c=1.0, ab=2.0, ac=2.0, bc=2.0, abc=1.0, normalize=1.0)
   >>> _ = v3.plot()
   >>> plt.show()


And you can do multiple plots by passing an axis object to plot.

.. plot::
  :include-source: true
  :context: reset

  >>> import matplotlib.pyplot as plt
  >>> import attr
  >>> from charticle.venn import Venn3
  >>> fig = plt.figure()
  >>> fig.set_size_inches(6,13)
  >>> v = Venn3(a="mathematics", b="substantive\nexpertise",
  ...  c="hacking\nskills",
  ...  fontsizes=Venn3.FontSizes(intersections=10),
  ...  sizes=Venn3.Sizes(normalize=30))
  >>> ax1, ax2, ax3, ax4 = (fig.add_subplot(411), fig.add_subplot(412),
  ...   fig.add_subplot(413), fig.add_subplot(414))
  >>> v.ab = "traditional\nresearch"; _ = v.plot(ax1)
  >>> v.ac = "machine\nlearning"; _ = v.plot(ax2)
  >>> v.bc = "danger\nzone!"; _ = v.plot(ax3)
  >>> v.abc = "data\nscience"; _ = v.plot(ax4)
  >>> # plt.subplots_adjust(wspace=)

