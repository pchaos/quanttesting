# -*- coding: utf-8 -*-
import backtrader as bt
import backtrader.indicators as btind

class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, movav=bt.ind.MovAv.Simple)

    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,

        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[1.0, -1.0],

        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[1.0, -1.0])

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(overunder=dict(ls='--'))

    def _plotlabel(self):
        # This method returns a list of labels that will be displayed
        # behind the name of the indicator on the plot

        # The period must always be there
        plabels = [self.p.period]

        # Put only the moving average if it's not the default one
        plabels += [self.p.movav] * self.p.notdefault('movav')

        return plabels

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        self.l.overunder = bt.Cmp(movav, self.data)
