"""
Tax-Calculator functions that calculate FICA and individual income taxes.
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 functions.py
# pylint --disable=locally-disabled --extension-pkg-whitelist=numpy function.py
# (when importing numpy, add "--extension-pkg-whitelist=numpy" pylint option)
#
# pylint: disable=too-many-lines
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


import pandas as pd
import math
import numpy as np
from .decorators import iterate_jit, jit
import copy


@iterate_jit(nopython=True)
def EI_FICA(SS_Earnings_c, e00200, e00200p, e00200s,
            e11055, e00250, e30100, FICA_ss_trt, FICA_mc_trt,
            e00900p, e00900s, e02100p, e02100s):
    """
    EI_FICA function: computes total earned income and regular FICA taxes.
    """
    # compute _sey
    sey_p = e00900p + e02100p
    sey_s = e00900s + e02100s
    _sey = sey_p + sey_s  # total self-employment income for filing unit

    # compute taxable earnings for OASDI FICA ('was' denotes 'wage and salary')
    sey_frac = 1.0 - 0.5 * (FICA_ss_trt + FICA_mc_trt)
    txearn_was_p = min(SS_Earnings_c, e00200p)
    txearn_was_s = min(SS_Earnings_c, e00200s)
    txearn_sey_p = min(max(0., sey_p * sey_frac), SS_Earnings_c - txearn_was_p)
    txearn_sey_s = min(max(0., sey_s * sey_frac), SS_Earnings_c - txearn_was_s)

    # compute OASDI FICA taxes for was and sey taxable earnings separately
    fica_ss_was_p = FICA_ss_trt * txearn_was_p
    fica_ss_was_s = FICA_ss_trt * txearn_was_s
    fica_ss_sey_p = FICA_ss_trt * txearn_sey_p
    fica_ss_sey_s = FICA_ss_trt * txearn_sey_s

    # compute regular HI FICA taxes for all was and sey earnings separately
    fica_mc_was_p = FICA_mc_trt * e00200p
    fica_mc_was_s = FICA_mc_trt * e00200s
    fica_mc_sey_p = FICA_mc_trt * max(0., sey_p * sey_frac)
    fica_mc_sey_s = FICA_mc_trt * max(0., sey_s * sey_frac)

    # compute total regular FICA taxes for filing unit
    fica_ss = fica_ss_was_p + fica_ss_was_s + fica_ss_sey_p + fica_ss_sey_s
    fica_mc = fica_mc_was_p + fica_mc_was_s + fica_mc_sey_p + fica_mc_sey_s
    _fica = fica_ss + fica_mc

    # compute regular FICA taxes on wage-and-salary income
    _fica_was = fica_ss_was_p + fica_ss_was_s + fica_mc_was_p + fica_mc_was_s

    # compute AGI deduction for "employer share" of self-employment FICA taxes
    c09400 = fica_ss_sey_p + fica_ss_sey_s + fica_mc_sey_p + fica_mc_sey_s
    c03260 = 0.5 * c09400  # half of c09400 represents the "employer share"

    # compute _earned
    c11055 = e11055
    _earned = max(0., e00200 + e00250 + c11055 + e30100 + _sey - c03260)

    return (_sey, _fica, _fica_was, c09400, c03260, c11055, _earned)


@iterate_jit(nopython=True)
def Adj(e35300_0, e35600_0, e35910_0, e03150, e03210, e03600, e03260, c03260,
        e03270, e03300, e03400, e03500, e03280, e03900, e04000, _exact,
        e03700, e03220, e03230, e03240, e03290, ALD_StudentLoan_HC,
        ALD_SelfEmploymentTax_HC, ALD_SelfEmp_HealthIns_HC, ALD_KEOGH_SEP_HC,
        ALD_EarlyWithdraw_HC, ALD_Alimony_HC):
    """
    Adj function:

    Adjustments: Form 1040, Form 2555.
    Calculates foreign earned income and total adjustments

    Notes
    -----
    Taxpayer characteristics:
        e03210 : Student loan interst deduction

        e03220 : Education Expense deduction

        e03150 : Total deduction IRS payments

        e03230 : Education credit adjustments

        e03240 : Domestic Production Activity Deduction

        e03270 : Self employed health insurance deduction

        e03290 : HSA deduction computer amount

        e03300 : Payments to a KEOGH plan and SEP deduction

        e03400 : Forfeited interest penalty early withdraw

        e03500 : Alimony withdraw

    Tax law parameters:
        ALD_StudentLoan_HC : Deduction for student loan interest haircut

        ALD_SelfEmploymentTax_HC : Deduction for self-employment tax haircut

        ALD_SelfEmp_HealthIns_HC :
        Deduction for self employed health insurance haircut

        ALD_KEOGH_SEP_HC :
        Deduction for payment to either KEOGH or SEP plan haircut

        ALD_EarlyWithdraw_HC : Deduction for forfeited interest penalty haricut

        ALD_Alimony_HC : Deduction for alimony payment haircut


    Returns
    -------
    _feided
        Foreign earned income deduction
    c02900
        total adjustments

    """
    # Form 2555: Foreign earned income
    _feided = max(e35300_0, e35600_0 + e35910_0)
    if _exact == 1:
        c03260 = e03260
    # For 1040: adjustments
    c02900 = (e03150 + (1 - ALD_StudentLoan_HC) * e03210 + e03600 +
              (1 - ALD_SelfEmploymentTax_HC) * c03260 +
              (1 - ALD_SelfEmp_HealthIns_HC) * e03270 +
              (1 - ALD_KEOGH_SEP_HC) * e03300 + (1 - ALD_EarlyWithdraw_HC) *
              e03400 + (1 - ALD_Alimony_HC) * e03500 + e03280 + e03900 +
              e04000 + e03700 + e03220 + e03230 + e03240 + e03290)
    return (_feided, c02900)


@iterate_jit(nopython=True)
def CapGains(p23250, p22250, e23660, _sep, _feided, FEI_ec_c, ALD_Interest_ec,
             ALD_StudentLoan_HC, f2555, e00200, e00300, e00600, e00700, e00800,
             e00900, e01100, e01200, e01400, e01700, e02000, e02100,
             e02300, e02600, e02610, e02800, e02540, e00400, e02400,
             c02900, e03210, e03230, e03240, e02615):
    """
    CapGains function: ...
    """
    # Net capital gain (long term + short term) before exclusion
    c23650 = p23250 + p22250 + e23660
    # Limitation for capital loss
    c01000 = max((-3000. / _sep), c23650)
    # Foreign earned income exclusion
    c02700 = min(_feided, FEI_ec_c * f2555)
    # compute _ymod* variables
    _ymod1 = (e00200 + (1 - ALD_Interest_ec) * e00300 + e00600 + e00700 +
              e00800 + e00900 + c01000 + e01100 + e01200 + e01400 + e01700 +
              e02000 + e02100 + e02300 + e02600 + e02610 + e02800 - e02540)
    _ymod2 = e00400 + (0.50 * e02400) - c02900
    _ymod3 = (1 - ALD_StudentLoan_HC) * e03210 + e03230 + e03240 + e02615
    _ymod = _ymod1 + _ymod2 + _ymod3
    return (c23650, c01000, c02700, _ymod1, _ymod2, _ymod3, _ymod)


@iterate_jit(nopython=True)
def SSBenefits(SSIND, MARS, e02500, _ymod, e02400, SS_thd50, SS_thd85,
               SS_percentage1, SS_percentage2):
    """
    SSBenefits function: ...
    """
    if SSIND == 2 or MARS == 3 or MARS == 6:
        c02500 = e02500
    elif _ymod < SS_thd50[MARS - 1]:
        c02500 = 0.
    elif _ymod >= SS_thd50[MARS - 1] and _ymod < SS_thd85[MARS - 1]:
        c02500 = SS_percentage1 * min(_ymod - SS_thd50[MARS - 1], e02400)
    else:
        c02500 = min(SS_percentage2 * (_ymod - SS_thd85[MARS - 1]) +
                     SS_percentage1 *
                     min(e02400, SS_thd85[MARS - 1] -
                         SS_thd50[MARS - 1]), SS_percentage2 * e02400)
    return (c02500, e02500)


@iterate_jit(nopython=True)
def AGI(_ymod1, c02500, c02700, e02615, c02900, e00100, e02500, XTOT,
        II_em, II_em_ps, MARS, _sep, II_prt, DSI):
    """
    AGI function: compute Adjusted Gross Income
    """
    c02650 = _ymod1 + c02500 - c02700 + e02615  # Gross Income
    c00100 = c02650 - c02900
    _agierr = e00100 - c00100  # Adjusted Gross Income
    _posagi = max(c00100, 0)
    _ywossbe = e00100 - e02500
    _ywossbc = c00100 - c02500
    _prexmp = XTOT * II_em
    if DSI:
        _prexmp = 0.
    # Personal Exemptions (_phaseout smoothed)
    _dispc_numer = II_prt * (_posagi - II_em_ps[MARS - 1])
    _dispc_denom = 2500. / _sep
    _dispc = min(1., max(0., _dispc_numer / _dispc_denom))
    c04600 = _prexmp * (1. - _dispc)
    return (c02650, c00100, _agierr, _posagi, _ywossbe, _ywossbc, _prexmp,
            c04600)


@iterate_jit(nopython=True, puf=True)
def ItemDed(_posagi, e17500, e18400, e18500, e18800, e18900, e19700,
            e20500, e20400, e19200, e20550, e20600, e20950, e19500, e19570,
            e19400, e19550, e19800, e20100, e20200, e20900, e21000, e21010,
            MARS, c00100, ID_ps, ID_Medical_frt, ID_Medical_HC,
            ID_Casualty_frt, ID_Casualty_HC, ID_Miscellaneous_frt,
            ID_Miscellaneous_HC, ID_Charity_crt_Cash, ID_Charity_crt_Asset,
            ID_prt, ID_crt, ID_StateLocalTax_HC, ID_Charity_frt,
            ID_Charity_HC, ID_InterestPaid_HC, ID_RealEstate_HC, puf):
    """
    ItemDed function:

    Itemized Deduction; Form 1040, Schedule A

    Notes
    -----
    Tax Law Parameters:
        ID_ps : Itemized deduction phaseout AGI start (Pease)

        ID_crt : Itemized deduction maximum phaseout
        as a percent of total itemized deduction (Pease)

        ID_prt : Itemized deduction phaseout rate (Pease)

        ID_Medical_frt : Deduction for medical expenses;
        floor as a percent of AGI

        ID_Casualty_frt : Deduction for casualty loss;
        floor as a percent of AGI

        ID_Miscellaneous_frt : Deduction for miscellaneous expenses;
        floor as a percent of AGI

        ID_Charity_crt_Cash : Deduction for charitable cash contributions;
        ceiling as a percent of AGI

        ID_Charity_crt_Asset : Deduction for charitable asset contributions;
        ceiling as a percent of AGI

        ID_Charity_frt : Deduction for charitable contributions;
        floor as a percent of AGI

    Taxpayer Characteristics:
        e17500 : Medical expense

        e18425 : Income taxes

        e18450 : General Sales Tax

        e18500 : Real Estate tax

        e19200 : Total interest deduction

        e19800 : Cash Contribution

        e19550 : Qualified Mortgage Insurance Premiums

        e20100 : Charity non-cash contribution

        e20400 : Total Miscellaneous expense

        e20550 : Unreimbursed employee business Expense

        e20600 : Tax preparation fee

    Intermediate Variables:
        _posagi: positive AGI

    Returns
    -------
    c04470 : Itemized deduction amount

    Warning
    -------
    Any additional keyword args, such as 'puf=True' here, must be
    passed to the function at the END of the argument list. If you stick the
    argument somewhere in the middle of the signature, you will get errors.
    """
    # Medical
    c17750 = ID_Medical_frt * _posagi
    c17000 = max(0., e17500 - c17750)
    # State and Local Income Tax, or Sales Tax
    _statax = (1 - ID_StateLocalTax_HC) * max(e18400, 0.)
    # Other Taxes (including state and local)
    real_estate = (1 - ID_RealEstate_HC) * e18500
    c18300 = _statax + real_estate + e18800 + e18900
    # Casualty
    if e20500 > 0:
        c37703 = e20500 + ID_Casualty_frt * _posagi
    else:
        c37703 = 0.
    c20500 = max(0., c37703 - ID_Casualty_frt * _posagi)
    # Miscellaneous
    c20750 = ID_Miscellaneous_frt * _posagi
    if puf:
        c20400 = e20400
    else:
        c20400 = e20550 + e20600 + e20950
    c20800 = max(0., c20400 - c20750)
    # Interest paid deduction
    if puf:
        c19200 = e19200
    else:
        c19200 = e19500 + e19570 + e19400 + e19550
    # Charity (assumes carryover is non-cash)
    base_charity = e19800 + e20100 + e20200
    if puf:
        c19700 = e19700
    elif base_charity <= 0.2 * _posagi:
        c19700 = base_charity
    else:
        lim30 = min(ID_Charity_crt_Asset * _posagi, e20100 + e20200)
        c19700 = min(ID_Charity_crt_Cash * _posagi, lim30 + e19800)
    charity_floor = ID_Charity_frt * _posagi  # frt is zero in present law
    c19700 = max(0., c19700 - charity_floor)
    # Gross Itemized Deductions
    c21060 = (e20900 + (1 - ID_Medical_HC) * c17000 + c18300 +
              (1 - ID_InterestPaid_HC) * c19200 +
              (1 - ID_Charity_HC) * c19700 +
              (1 - ID_Casualty_HC) * c20500 +
              (1 - ID_Miscellaneous_HC) * c20800 +
              e21000 + e21010)
    # Limitations on deductions excluding medical, charity etc
    _phase2_i = ID_ps[MARS - 1]
    _nonlimited = ((1 - ID_Medical_HC) * c17000 +
                   (1 - ID_Casualty_HC) * c20500 +
                   e19570 + e21010 + e20900)
    _limitratio = _phase2_i
    # Itemized deductions amount after limitation if any
    c04470 = c21060
    if c21060 > _nonlimited and c00100 > _limitratio:
        dedmin = ID_crt * (c21060 - _nonlimited)
        dedpho = ID_prt * max(0., _posagi - _limitratio)
        c21040 = min(dedmin, dedpho)
        c04470 = c21060 - c21040
    else:
        c21040 = 0.
    return (c17750, c17000, _statax, c18300, c37703, c20500,
            c20750, c20400, c19200, c20800, c19700, c21060, _phase2_i,
            _nonlimited, _limitratio, c04470, c21040)


@iterate_jit(nopython=True)
def AMED(_fica, e00200, MARS, AMED_thd, _sey, AMED_trt,
         FICA_mc_trt, FICA_ss_trt):
    """
    AMED function: computes additional Medicare Tax as a part of FICA

    Notes
    -----
    Tax Law Parameters:
        AMED_thd : Additional medicare threshold

        AMED_trt : Additional medicare tax rate

        FICA_ss_trt : FICA social security tax rate

        FICA_mc_trt : FICA medicare tax rate

    Taxpayer Charateristics:
        e00200 : Total wages and salaries

        _sey : Business and Farm net income/loss

    Returns
    -------
    _amed : Additional medicare tax amount

    """
    # ratio of income subject to AMED tax = (1 - 0.5*(FICA_mc_trt+FICA_ss_trt)
    _amed = AMED_trt * (max(0., e00200 - AMED_thd[MARS - 1]) +
                        max(0., max(0., _sey) *
                            (1. - 0.5 * (FICA_mc_trt + FICA_ss_trt)) -
                            max(0., AMED_thd[MARS - 1] - e00200)))
    _fica = _fica + _amed
    return (_amed, _fica)


@iterate_jit(nopython=True)
def StdDed(DSI, _earned, STD, p04470, e00100, e60000, age_head, age_spouse,
           MARS, MIDR, e15360, blind_head, blind_spouse, _exact, e04200,
           STD_Aged, f6251):
    """
    StdDed function:

    Standard Deduction; Form 1040

    This function calculates standard deduction,
    including standard deduction for dependents, aged and bind.

    Notes
    -----
    Tax Law Parameters:
        STD : Standard deduction amount, filing status dependent

        STD_Aged : Additional standard deduction for blind and aged

        II_brk* : Personal income tax bracket upper thresholds: range 1-6

        II_rt* : Personal income tax rates: range 1-7,
        respectively for lowest income bracket to the highest

    Taxpayer Characteristics:
        _earned : (F2441) Earned income amount

        e02400 : Gross social Security Benefit

        e60000 : AMT taxable income

        DSI : Dependent Status Indicator:
            0 - not being claimed as a dependent
            1 - claimed as a dependent

        MIDR : Married filing separately itemized deductions
        requirement indicator:
            0 - not necessary to itemize because of filing status
            1 - necessary to itemize when filing separately

    Returns
    -------
    _standard
        Standard deduction amount for each taxpayer
        who files standard deduction. Otherwise value is zero.
    """
    # Calculate deduction for dependents
    if DSI == 1:
        c15100 = max(350. + _earned, STD[6])
        c04100 = min(STD[MARS - 1], c15100)
    else:
        c15100 = 0.
        if MIDR == 1:
            c04100 = 0.
        else:
            c04100 = STD[MARS - 1]
    # Add motor vehicle tax to standard deduction
    c04100 = c04100 + e15360
    # ??
    x04500 = 0.
    if f6251 == 0 and p04470 == 0:
        x04500 = e00100 - e60000
    # Calculate extra standard deduction for aged and blind
    _extrastd = blind_head + blind_spouse
    if age_head >= 65:
        _extrastd += 1
    if MARS == 2 and age_spouse >= 65:
        _extrastd += 1
    if _exact == 1 and MARS == 3 or MARS == 5:
        c04200 = e04200
    else:
        c04200 = _extrastd * STD_Aged[MARS - 1]
    c15200 = c04200
    # Compute the total standard deduction
    _standard = c04100 + c04200
    if (MARS == 3 or MARS == 6) and (MIDR == 1):
        _standard = 0.
    return (_standard, c04200, c15200, c15100, x04500, c04100)


@iterate_jit(nopython=True)
def TaxInc(c00100, _standard, e37717, c21060, c21040, c04500, c04600,
           e04805, _feided, c04800, MARS,
           II_rt1, II_rt2, II_rt3, II_rt4,
           II_rt5, II_rt6, II_rt7, II_brk1, II_brk2, II_brk3,
           II_brk4, II_brk5, II_brk6, c02700):
    """
    TaxInc function: ...
    """
    c04500 = max(0., c00100 - max(c21060 - c21040, _standard + e37717))
    c04800 = max(0., c04500 - c04600 - e04805)
    # Some taxpayers iteimize only for AMT, not regular tax
    _amtstd = 0.
    if c04800 > 0. and _feided > 0.:
        _taxinc = c04800 + c02700
    else:
        _taxinc = c04800
    if c04800 > 0. and _feided > 0.:
        _feitax = Taxer_i(_feided, MARS, II_rt1, II_rt2, II_rt3, II_rt4,
                          II_rt5, II_rt6, II_rt7, II_brk1, II_brk2, II_brk3,
                          II_brk4, II_brk5, II_brk6)
        _oldfei = Taxer_i(c04800, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5,
                          II_rt6, II_rt7, II_brk1, II_brk2, II_brk3, II_brk4,
                          II_brk5, II_brk6)
    else:
        _feitax, _oldfei = 0., 0.
    return (c04500, c04800, _amtstd, _taxinc, _feitax, _oldfei, _standard)


@iterate_jit(nopython=True)
def Personal_Credit(c04500, MARS, II_credit, II_credit_ps, II_credit_prt):
    """
    Personal_Credit function: ...
    """
    # full amount as defined in the parameter
    _personal_credit = II_credit[MARS - 1]
    # phaseout using taxable income
    if c04500 > II_credit_ps[MARS - 1]:
        credit_phaseout = II_credit_prt * (c04500 - II_credit_ps[MARS - 1])
    else:
        credit_phaseout = 0.
    _personal_credit = max(0., _personal_credit - credit_phaseout)
    return _personal_credit


@iterate_jit(nopython=True)
def XYZD(_taxinc, c04800, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5, II_rt6,
         II_rt7, II_brk1, II_brk2, II_brk3, II_brk4, II_brk5, II_brk6):
    """
    XYZD function: ...
    """
    _xyztax = Taxer_i(_taxinc, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5,
                      II_rt6, II_rt7, II_brk1, II_brk2, II_brk3, II_brk4,
                      II_brk5, II_brk6)
    c05200 = Taxer_i(c04800, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5,
                     II_rt6, II_rt7, II_brk1, II_brk2, II_brk3, II_brk4,
                     II_brk5, II_brk6)
    return (_xyztax, c05200)


@iterate_jit(nopython=True)
def NonGain(c23650, p23250, e01100):
    """
    NonGain function: ...
    """
    _cglong = min(c23650, p23250) + e01100
    _noncg = 0.
    return (_cglong, _noncg)


@iterate_jit(nopython=True)
def TaxGains(e00650, c01000, c04800, c23650, p23250, e01100, e58990,
             e58980, e24515, e24518, MARS, _taxinc, _xyztax, _feided,
             _feitax, _cmp, e59410, e59420, e59440, e59470, e59400,
             e83200_0, e10105, e74400, II_rt1, II_rt2, II_rt3, II_rt4,
             II_rt5, II_rt6, II_rt7,
             II_brk1, II_brk2, II_brk3, II_brk4, II_brk5, II_brk6,
             CG_rt1, CG_rt2, CG_rt3, CG_thd1, CG_thd2):
    """
    TaxGains function: ...
    """
    # pylint: disable=too-many-statements,too-many-branches
    c00650 = e00650
    _addtax = 0.
    if c01000 > 0. or c23650 > 0. or p23250 > 0. or e01100 > 0. or e00650 > 0.:
        _hasgain = 1
    else:
        _hasgain = 0
    if _hasgain == 1:
        # if/else 1
        _dwks5 = max(0., e58990 - e58980)
        c24505 = max(0., c00650 - _dwks5)
        # gain for tax computation
        if e01100 > 0.:
            c24510 = e01100
        else:
            c24510 = max(0., min(c23650, p23250)) + e01100
        _dwks9 = max(0., c24510 - min(e58990, e58980))
        c24516 = c24505 + _dwks9

        # if/else 2
        _dwks12 = min(_dwks9, e24515 + e24518)
        c24517 = c24516 - _dwks12
        c24520 = max(0., _taxinc - c24517)
        # tentative TI less schD gain
        c24530 = min(CG_thd1[MARS - 1], _taxinc)

        # if/else 3
        _dwks16 = min(c24520, c24530)
        _dwks17 = max(0., _taxinc - c24516)
        c24540 = max(_dwks16, _dwks17)
        c24534 = c24530 - _dwks16
        lowest_rate_tax = CG_rt1 * c24534
        _dwks21 = min(_taxinc, c24517)
        c24597 = max(0., _dwks21 - c24534)

        # if/else 4
        # income subject to 15% tax
        c24598 = CG_rt2 * c24597  # actual 15% tax
        _dwks25 = min(_dwks9, e24515)
        _dwks26 = c24516 + c24540
        _dwks28 = max(0., _dwks26 - _taxinc)
        c24610 = max(0., _dwks25 - _dwks28)
        c24615 = 0.25 * c24610
        _dwks31 = c24540 + c24534 + c24597 + c24610
        c24550 = max(0., _taxinc - _dwks31)
        c24570 = 0.28 * c24550

        if c24540 > CG_thd2[MARS - 1]:
            _addtax = (CG_rt3 - CG_rt2) * c24517

        elif c24540 <= CG_thd2[MARS - 1] and _taxinc > CG_thd2[MARS - 1]:
            _addtax = (CG_rt3 - CG_rt2) * min(_dwks21,
                                              _taxinc - CG_thd2[MARS - 1])

        c24560 = Taxer_i(c24540, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5,
                         II_rt6, II_rt7, II_brk1, II_brk2, II_brk3, II_brk4,
                         II_brk5, II_brk6)

        _taxspecial = (lowest_rate_tax + c24598 + c24615 + c24570 + c24560 +
                       _addtax)

        c24580 = min(_taxspecial, _xyztax)

    else:
        # these vars only to check accuracy? unused in calcs. (except c24580)
        _dwks5 = 0.
        _dwks9 = 0.
        c24505 = 0.
        c24510 = 0.
        c24516 = max(0., min(p23250, c23650)) + e01100

        _dwks12 = 0.
        c24517 = 0.
        c24520 = 0.
        c24530 = 0.

        _dwks16 = 0.
        _dwks17 = 0.
        c24540 = 0.
        c24534 = 0.
        _dwks21 = 0.
        c24597 = 0.

        c24598 = 0.
        _dwks25 = 0.
        _dwks26 = 0.
        _dwks28 = 0.
        c24610 = 0.
        c24615 = 0.
        _dwks31 = 0.
        c24550 = 0.
        c24570 = 0.
        _addtax = 0.
        c24560 = 0.
        _taxspecial = 0.
        c24580 = _xyztax

    if c04800 > 0. and _feided > 0.:
        c05100 = max(0., c24580 - _feitax)
    else:
        c05100 = c24580

    # Form 4972, Lump Sum Distributions
    if _cmp == 1:
        c59430 = max(0., e59410 - e59420)
        c59450 = c59430 + e59440  # income plus lump sum
        c59460 = (max(0., min(0.5 * c59450, 10000.)) - 0.2 *
                  max(0., 59450. - 20000.))
        _line17 = c59450 - c59460
        _line19 = c59450 - c59460 - e59470
        if c59450 >= 0.:
            _line22 = max(0., e59440 - e59440 * c59460 / c59450)
        else:
            _line22 = 0.
        _line30 = 0.1 * max(0., c59450 - c59460 - e59470)
        _line31 = (0.11 * min(_line30, 1190.) +
                   0.12 * min(2270. - 1190., max(0., _line30 - 1190.)) +
                   0.14 * min(4530. - 2270., max(0., _line30 - 2270.)) +
                   0.15 * min(6690. - 4530., max(0., _line30 - 4530.)) +
                   0.16 * min(9170. - 6690., max(0., _line30 - 6690.)) +
                   0.18 * min(11440. - 9170., max(0., _line30 - 9170.)) +
                   0.20 * min(13710. - 11440., max(0., _line30 - 11440.)) +
                   0.23 * min(17160. - 13710., max(0., _line30 - 13710.)) +
                   0.26 * min(22880. - 17160., max(0., _line30 - 17160.)) +
                   0.30 * min(28600. - 22880., max(0., _line30 - 22880.)) +
                   0.34 * min(34320. - 28600., max(0., _line30 - 28600.)) +
                   0.38 * min(42300. - 34320., max(0., _line30 - 34320.)) +
                   0.42 * min(57190. - 42300., max(0., _line30 - 42300.)) +
                   0.48 * min(85790. - 57190., max(0., _line30 - 57190.)))
        _line32 = 10. * _line31
        if e59440 == 0.:
            _line36 = _line32
            # below are unused in calcs
            _line33 = 0.
            _line34 = 0.
            _line35 = 0.
        elif e59440 > 0.:
            _line33 = 0.1 * _line22
            _line34 = (0.11 * min(_line30, 1190.) +
                       0.12 * min(2270. - 1190., max(0., _line30 - 1190.)) +
                       0.14 * min(4530. - 2270., max(0., _line30 - 2270.)) +
                       0.15 * min(6690. - 4530., max(0., _line30 - 4530.)) +
                       0.16 * min(9170. - 6690., max(0., _line30 - 6690.)) +
                       0.18 * min(11440. - 9170., max(0., _line30 - 9170.)) +
                       0.20 * min(13710. - 11440., max(0., _line30 - 11440.)) +
                       0.23 * min(17160. - 13710., max(0., _line30 - 13710.)) +
                       0.26 * min(22880. - 17160., max(0., _line30 - 17160.)) +
                       0.30 * min(28600. - 22880., max(0., _line30 - 22880.)) +
                       0.34 * min(34320. - 28600., max(0., _line30 - 28600.)) +
                       0.38 * min(42300. - 34320., max(0., _line30 - 34320.)) +
                       0.42 * min(57190. - 42300., max(0., _line30 - 42300.)) +
                       0.48 * min(85790. - 57190., max(0., _line30 - 57190.)))
            _line35 = 10. * _line34
            _line36 = max(0., _line32 - _line35)
        else:
            _line33 = 0.
            _line34 = 0.
            _line35 = 0.
            _line36 = 0.
        # tax saving from 10 yr option
        c59485 = _line36
        c59490 = c59485 + 0.2 * max(0., e59400)
        # pension gains tax plus
        c05700 = c59490
    else:
        # all but one unused in calcs
        c59430 = 0.
        c59450 = 0.
        c59460 = 0.
        _line17 = 0.
        _line19 = 0.
        _line22 = 0.
        _line30 = 0.
        _line31 = 0.
        _line32 = 0.
        _line33 = 0.
        _line34 = 0.
        _line35 = 0.
        _line36 = 0.
        c59485 = 0.
        c59490 = 0.
        c05700 = 0.
    _parents = e83200_0
    _s1291 = e10105
    c05750 = max(c05100 + _parents + c05700, e74400)
    _taxbc = c05750
    return (c00650, _hasgain, _dwks5, c24505, c24510, _dwks9, c24516,
            c24580, _dwks12, c24517, c24520, c24530, _dwks16,
            _dwks17, c24540, c24534, _dwks21, c24597, c24598, _dwks25,
            _dwks26, _dwks28, c24610, c24615, _dwks31, c24550, c24570,
            _addtax, c24560, _taxspecial, c05100, c05700, c59430,
            c59450, c59460, _line17, _line19, _line22, _line30, _line31,
            _line32, _line36, _line33, _line34, _line35, c59485, c59490,
            _s1291, _parents, _taxbc, c05750)


@iterate_jit(nopython=True, puf=True)
def AMTI(c60000, _exact, e60290, _posagi, e07300, c24517,
         e60300, e60860, p60100, e60840, e60630, e60550, FDED,
         e60720, e60430, e60500, e60340, e60680, e60600, e60405,
         e60440, e60420, e60410, e61400, e60660, e60480, c21060,
         e62000, e60250, _cmp, _standard, p04470,
         f6251, c00100, e60000, t04470,
         c04470, c17000, e18500, c20800, c21040, e04805,
         c02700,
         e24515, x60130, e18400,
         x60220, x60240, c18300, _taxbc, AMT_tthd, AMT_CG_thd1, AMT_CG_thd2,
         MARS, _sep, AMT_Child_em, AMT_CG_rt1,
         AMT_CG_rt2, AMT_CG_rt3, AMT_em_ps, AMT_em_pe, x62720, e00700, c24516,
         c24520, c05700, e05800, e05100,
         age_head, KT_c_Age, e62900, AMT_thd_MarriedS, _earned, e62600,
         AMT_em, AMT_prt, AMT_trt1, AMT_trt2, _cmbtp_itemizer,
         _cmbtp_standard, ID_StateLocalTax_HC, ID_Medical_HC,
         ID_Miscellaneous_HC, ID_RealEstate_HC, puf):
    """
    AMTI function: ...
    """
    # pylint: disable=too-many-statements,too-many-branches

    # if e62720 != 0 and e24517 > 0:
    #    x62720 = e62720 - e24517
    c62720 = c24517 + x62720
    # if e60260 != 0 and e00700 > 0:
    #    x60260 = e60260 - e00700
    c60260 = e00700
    # QUESTION: c63100 variable is reassigned below before use, is this a BUG?
    c63100 = max(0., _taxbc - e07300)
    c60200 = min((1 - ID_Medical_HC) * c17000, 0.025 * _posagi)
    # if e60240 != 0 and e18300 > 0:
    #    x60240 = e60240 - e18300
    c60240 = c18300 + x60240
    # if e60220 != 0 and e20800 > 0:
    #    x60220 = e60220 - e20800
    c60220 = (1 - ID_Miscellaneous_HC) * c20800 + x60220
    # if e60130 != 0 and e21040 > 0:
    #    x60130 = e60130 - e21040
    c60130 = c21040 + x60130
    c62730 = e24515
    if FDED == 2:
        _prefded = 0.
    else:
        _prefded = c60200 + c60220 + c60240
    _prefnot = c21060 - c21040 - _prefded
    _totded = _prefded + _prefnot
    if FDED == 1:
        c60000 = c00100 - _totded
    elif FDED == 3:
        c60000 = c00100 - max(c04470, t04470)
    else:
        c60000 = c00100
    c60000 = c60000 - e04805
    if FDED == 1 or ((_prefded + e60290) > 0):
        _addamt = _prefded + e60290 - c60130
    else:
        _addamt = 0.
    if _cmp == 1:
        c62100 = (_addamt + e60300 + e60860 + p60100 + e60840 + e60630 +
                  e60550 + e60720 + e60430 + e60500 + e60340 + e60680 +
                  e60600 + e60405 + e60440 + e60420 + e60410 + e61400 +
                  e60660 - c60260 - e60480 - e62000 + c60000 - e60250)
    if puf and ((_standard == 0 or (_exact == 1 and p04470 > 0.))):
        if f6251 == 1:
            _cmbtp = _cmbtp_itemizer
        else:
            _cmbtp = 0.
        real_estate = (1 - ID_RealEstate_HC) * e18500
        income_sales = (1 - ID_StateLocalTax_HC) * max(0., e18400)
        c62100 = (c00100 - c04470 +
                  max(0., min((1 - ID_Medical_HC) * c17000, 0.025 * c00100)) +
                  income_sales + real_estate -
                  c60260 + (1 - ID_Miscellaneous_HC) * c20800 - c21040)
        c62100 += _cmbtp
    if puf and _standard > 0:
        if f6251 == 1:
            _cmbtp = _cmbtp_standard
        else:
            _cmbtp = 0.
        c62100 = c00100 - c60260
        c62100 += _cmbtp
    if MARS == 3 or MARS == 6:
        _amtsepadd = max(0.,
                         min(AMT_thd_MarriedS, 0.25 * (c62100 - AMT_em_pe)))
    else:
        _amtsepadd = 0.
    c62100 = c62100 + _amtsepadd
    c62600 = max(0., AMT_em[MARS - 1] - AMT_prt *
                 max(0., c62100 - AMT_em_ps[MARS - 1]))
    if _cmp == 1 and f6251 == 1 and _exact == 1:
        c62600 = e62600
    if age_head != 0 and age_head < KT_c_Age:
        c62600 = min(c62600, _earned + AMT_Child_em)
    c62700 = max(0., c62100 - c62600)
    if c02700 > 0.:
        _alminc = max(0., c62100 - c62600)
        _amtfei = (AMT_trt1 * c02700 + AMT_trt2 *
                   max(0., (c02700 - (AMT_tthd / _sep))))
    else:
        _alminc = c62700
        _amtfei = 0.
    c62780 = (AMT_trt1 * _alminc + AMT_trt2 *
              max(0., (_alminc - (AMT_tthd / _sep) - _amtfei)))
    if f6251 == 1:
        c62900 = e62900
    else:
        c62900 = e07300
    if c24516 == 0.:
        c62740 = c62720 + c62730
    else:
        c62740 = min(max(0., c24516), c62720 + c62730)
    _ngamty = max(0., _alminc - c62740)
    c62745 = (AMT_trt1 * _ngamty +
              AMT_trt2 * max(0., (_ngamty - (AMT_tthd / _sep))))
    # Capital Gain for AMT
    _tamt2 = 0.
    _amt5pc = 0.
    _line45 = max(0., AMT_CG_thd1[MARS - 1] - c24520)
    _line46 = min(_alminc, c62720)
    _line47 = min(_line45, _line46)
    _line48 = min(_alminc, c62720) - _line47
    _amt15pc = min(_line48, max(0., AMT_CG_thd2[MARS - 1] - c24520 - _line45))
    if _ngamty != (_amt15pc + _line47):
        _amt20pc = _line46 - _amt15pc - _line47
    else:
        _amt20pc = 0.
    if c62740 != 0.:
        _amt25pc = max(0., _alminc - _ngamty - _line46)
    else:
        _amt25pc = 0.
    c62747 = AMT_CG_rt1 * _amt5pc
    c62755 = AMT_CG_rt2 * _amt15pc
    c62760 = AMT_CG_rt3 * _amt20pc
    c62770 = 0.25 * _amt25pc  # tax rate on "Unrecaptured Schedule E Gain"
    _tamt2 = c62747 + c62755 + c62760 + c62770  # line62 without 42 being added
    c62800 = min(c62780, c62745 + _tamt2 - _amtfei)
    c63000 = c62800 - c62900
    c63100 = _taxbc - e07300 - c05700
    c63100 = max(0., c63100)
    c63200 = max(0., c63000 - c63100)
    c09600 = c63200
    # no _othtax in SAS
    _othtax = e05800 - (e05100 + c09600)
    c62100_everyone = c62100
    if c09600 == 0. and e60000 == 0.:
        c60000 = 0.
        c62100 = 0.
    c05800 = _taxbc + c63200
    return (c62720, c60260, c63100, c60200, c60240, c60220, c60000,
            c60130, c62730, _addamt, c62100,
            _amtsepadd, c62600, c62700, c62760,
            _alminc, _amtfei, c62780, c62900, c63000, c62740,
            _ngamty, c62745, _tamt2, _amt5pc, _amt15pc,
            _amt25pc, c62747, c62755, c62770, _amt20pc, c62800,
            c09600, _othtax, c05800, _cmbtp, c62100_everyone)


@iterate_jit(nopython=True)
def MUI(c00100, NIIT_thd, MARS, e00300, e00600, c01000, e02000, NIIT_trt,
        NIIT, e85070, e26270):
    """
    MUI function: ...
    """
    NIIT = NIIT_trt * min(e00300 + e00600 + max(0., c01000) +
                          max(0., e02000 - e26270 + e85070),
                          max(0., c00100 - NIIT_thd[MARS - 1]))
    return NIIT


@iterate_jit(nopython=True, puf=True)
def F2441(_earned, _fixeic, e59560, MARS, f2441, DCC_c, e00200p, e00200s,
          e32800, puf):
    """
    F2441 function: ...
    """
    if _fixeic == 1:
        _earned = e59560
    if MARS == 2 and puf:
        c32880 = e00200p
        c32890 = e00200s
    else:
        c32880 = _earned
        c32890 = _earned
    _dclim = min(f2441, 2.) * DCC_c
    c32800 = min(e32800, _dclim)
    return (_earned, c32880, c32890, _dclim, c32800)


@iterate_jit(nopython=True)
def DepCareBen(c32800, _cmp, f2441, MARS, c32880, c32890, e33420, e33430,
               e33450, e33460, e33465, e33470, _sep, _dclim):
    """
    DepCareBen function: ...
    """
    # Part III of dependent care benefits
    if f2441 != 0 and MARS == 2:
        _seywage = min(c32880, c32890, e33420 + e33430 - e33450, e33460)
    else:
        _seywage = 0.
    if _cmp == 1 and MARS != 2:  # this is same as above, why?
        _seywage = min(c32880, c32890, e33420 + e33430 - e33450, e33460)
    if f2441 != 0:
        c33465 = e33465
        c33470 = e33470
        c33475 = max(0., min(_seywage, (5000. / _sep)) - c33470)
        c33480 = max(0., e33420 + e33430 - e33450 - c33465 - c33475)
        c32840 = c33470 + c33475
        c32800 = min(max(0., _dclim - c32840), max(0., c32800 - c32840))
    else:
        c33465, c33470, c33475, c33480, c32840 = 0., 0., 0., 0., 0.
        c32800 = c32800
    c33000 = max(0., min(c32800, min(c32880, c32890)))
    return (_seywage, c33465, c33470, c33475, c33480, c32840, c32800, c33000)


@iterate_jit(nopython=True)
def ExpEarnedInc(_exact, c00100, CDCC_ps, CDCC_crt,
                 c33000, c05800, e07300, f2441):
    """
    ExpEarnedInc function: ...
    """
    # Expenses limited to earned income
    if _exact == 1:
        _tratio = math.ceil(max(((c00100 - CDCC_ps) / 2000.), 0.))
        c33200 = c33000 * 0.01 * max(20., CDCC_crt - min(15., _tratio))
    else:
        _tratio = 0.
        c33200 = c33000 * 0.01 * max(20., CDCC_crt -
                                     max(((c00100 - CDCC_ps) / 2000.), 0.))
    c33400 = min(max(0., c05800 - e07300), c33200)
    # amount of the credit
    if f2441 == 0:
        c07180 = 0.
        c33000 = 0.
    else:
        c07180 = c33400
    return (_tratio, c33200, c33400, c07180, c33000)


@iterate_jit(nopython=True)
def NumDep(EIC, c00100, c01000, e00400, MARS, EITC_ps, EITC_MinEligAge,
           age_head, EITC_MaxEligAge, EITC_ps_MarriedJ, EITC_rt, c59560,
           EITC_c, age_spouse, EITC_prt, e83080, e00300, e00600, e40223,
           e25360, e25430, p25470, e25400, e25500, e26210, e26340, e27200,
           e26205, e26320, EITC_InvestIncome_c, _earned, c59660, _exact,
           e59560):
    """
    NumDep function: ...
    """
    # pylint: disable=too-many-branches
    _preeitc = 0.
    if _exact == 1:
        c59560 = e59560
    else:
        c59560 = _earned
    # Modified AGI only through 2002
    _modagi = c00100 + e00400
    if MARS == 2:
        _val_ymax = EITC_ps[EIC] + EITC_ps_MarriedJ[EIC]
    elif MARS == 1 or MARS == 4 or MARS == 5 or MARS == 7:
        _val_ymax = EITC_ps[EIC]
    else:
        _val_ymax = 0.
    if MARS == 1 or MARS == 4 or MARS == 5 or MARS == 2 or MARS == 7:
        c59660 = min(EITC_rt[EIC] * c59560, EITC_c[EIC])
        _preeitc = c59660
    if (MARS != 3 and MARS != 6 and
            (_modagi > _val_ymax or c59560 > _val_ymax)):
        _preeitc = max(0., EITC_c[EIC] - EITC_prt[EIC] *
                       (max(0., max(_modagi, c59560) - _val_ymax)))
        _preeitc = min(_preeitc, c59660)
    if MARS != 3 and MARS != 6:
        _val_rtbase = EITC_rt[EIC] * 100.
        _val_rtless = EITC_prt[EIC] * 100.
        _dy = (e00400 + e83080 + e00300 + e00600 +
               max(0., max(0., c01000) - max(0., e40223)) +
               max(0., max(0., e25360) - e25430 - p25470 - e25400 - e25500) +
               max(0., e26210 + e26340 + e27200 - e26205 - e26320))
    else:
        _val_rtbase = 0.
        _val_rtless = 0.
        _dy = 0.
    if MARS != 3 and MARS != 6 and _dy > EITC_InvestIncome_c:
        _preeitc = 0.

    if EIC == 0:
        # enforce age eligibility rule for those with no EITC-eligible children
        # (assume that an unknown age_* value implies EITC age eligibility)
        # pylint: disable=bad-continuation
        if MARS == 2:
            if (age_head >= EITC_MinEligAge and
                age_head <= EITC_MaxEligAge) or \
               (age_spouse >= EITC_MinEligAge and
                age_spouse <= EITC_MaxEligAge) or \
               age_head == 0 or \
               age_spouse == 0:
                c59660 = _preeitc
            else:
                c59660 = 0.
        else:
            if (age_head >= EITC_MinEligAge and
                age_head <= EITC_MaxEligAge) or \
               age_head == 0:
                c59660 = _preeitc
            else:
                c59660 = 0.
    else:
        c59660 = _preeitc

    if c59660 == 0:
        c59560 = 0.
    return (_modagi, c59560, c59660, _val_ymax,
            _preeitc, _val_rtbase, _val_rtless, _dy)


@iterate_jit(nopython=True)
def ChildTaxCredit(n24, MARS, CTC_c, c00100, _feided, CTC_ps, _exact,
                   _precrd, _nctcr, CTC_prt):
    """
    ChildTaxCredit function: ...
    """
    _nctcr = n24
    _precrd = CTC_c * _nctcr
    _ctcagi = c00100 + _feided
    if _ctcagi > CTC_ps[MARS - 1]:
        excess = _ctcagi - CTC_ps[MARS - 1]
        if _exact == 1:
            excess = 1000. * math.ceil(excess / 1000.)
        _precrd = max(0., _precrd - CTC_prt * excess)
    return (_nctcr, _precrd, _ctcagi)


@iterate_jit(nopython=True, puf=True)
def AmOppCr(p87482, e87487, e87492, e87497, p87521, puf):
    """
    American Opportunity Credit 2009+; Form 8863

    This function calculates American Opportunity Credit
    for up to four eligible students.
    """
    # Expense should not exceed the cap of $4000.
    c87482 = max(0., min(p87482, 4000.))
    c87487 = max(0., min(e87487, 4000.))
    c87492 = max(0., min(e87492, 4000.))
    c87497 = max(0., min(e87497, 4000.))
    # Credit calculated as 100% of the first $2000 expense plus
    # 25% of amount exceeding $2000.
    if max(0., c87482 - 2000.) == 0.:
        c87483 = c87482
    else:
        c87483 = 2000. + 0.25 * max(0., c87482 - 2000.)
    if max(0., c87487 - 2000.) == 0.:
        c87488 = c87487
    else:
        c87488 = 2000 + 0.25 * max(0., c87487 - 2000)
    if max(0., c87492 - 2000.) == 0.:
        c87493 = c87492
    else:
        c87493 = 2000. + 0.25 * max(0., c87492 - 2000.)
    if max(0., c87497 - 2000.) == 0.:
        c87498 = c87497
    else:
        c87498 = 2000. + 0.25 * max(0., c87497 - 2000.)
    # Sum of credits of all four students.
    c87521 = c87483 + c87488 + c87493 + c87498
    if puf:
        c87521 = p87521
    return (c87482, c87487, c87492, c87497, c87483, c87488, c87493, c87498,
            c87521)


@iterate_jit(nopython=True, puf=True)
def LLC(e87530, LLC_Expense_c, e87526, e87522, e87524, e87528, puf):
    """
    Lifetime Learning Credit; Form 8863

    Notes
    -----
    Tax Law Parameters that are not parameterized:

        0.2 : Lifetime Learning Credit ratio against expense:

    Tax Law Parameters that are parameterized:

        LLC_Expense_c : Lifetime Learning Credit expense limit

    Taxpayer Charateristics:

        e87530 : Total expense

        and four other e8752? values used only if puf is False

    Returns
    -------
        c87550 : Nonrefundable Education Credit

        and intermediate variables used to compute this credit amount
    """
    if puf:
        c87530 = 0.
        c87540 = min(e87530, LLC_Expense_c)
    else:
        c87530 = e87526 + e87522 + e87524 + e87528
        c87540 = min(c87530, LLC_Expense_c)
    c87550 = 0.2 * c87540
    return (c87540, c87550, c87530)


@iterate_jit(nopython=True)
def RefAmOpp(c87521, _num, c00100):
    """
    Refundable American Opportunity Credit 2009+; Form 8863

    This function checks the previously calculated American Opportunity Credit
    with the phaseout range and then applies the 0.4 refundable rate.

    Notes
    -----
    Tax Law Parameters that are not parameterized:

        90000 : American Opportunity Credit phaseout income base

        10000 : American Opportunity Credit phaseout income range length

        1/1000 : American Opportunity Credit phaseout rate

        0.4 : American Opportunity Credit refundable rate

    Parameters
    ----------
        c87521 : gross American Opportunity Credit

        _num : number of people filing jointly

        c00100 : AGI

    Returns
    -------
        c87666 : Refundable part of American Opportunity Credit

        c87668 : Nonrefundable part of American Opportunity Credit

        and intermediate variables used to compute these two credit amounts
    """
    if c87521 > 0:
        c87654 = 90000. * _num
        c87656 = c00100
        c87658 = max(0., c87654 - c87656)
        c87660 = 10000. * _num
        c87662 = 1000. * min(1., c87658 / c87660)
        c87664 = c87662 * c87521 / 1000.
        c87666 = 0.4 * c87664
        c10960 = c87666
        c87668 = c87664 - c87666
    else:
        c87654 = 0.
        c87656 = 0.
        c87658 = 0.
        c87660 = 0.
        c87662 = 0.
        c87664 = 0.
        c87666 = 0.
        c10960 = 0.
        c87668 = 0.
    return (c87654, c87656, c87658, c87660, c87662, c87664, c87666, c10960,
            c87668)


@iterate_jit(nopython=True)
def NonEdCr(c87550, MARS, ETC_pe_Married, c00100, _num, c07180, e07200, c07230,
            e07600, e07240, e07960, e07260, e07300, e07700, e07250, t07950,
            c05800, _precrd, ETC_pe_Single, c87668, c87620):
    """
    NonEdCr function: ...
    """
    # Nonrefundable Education Credits
    # Form 8863 Tentative Education Credits
    c87560 = c87550
    # Phase Out
    if MARS == 2:
        c87570 = ETC_pe_Married * 1000.
    else:
        c87570 = ETC_pe_Single * 1000.
    c87580 = c00100
    c87590 = max(0., c87570 - c87580)
    c87600 = 10000. * _num
    c87610 = min(1., c87590 / c87600)
    c87620 = c87560 * c87610
    _xlin4 = max(0., c05800 - (e07300 + c07180 + e07200))
    _xlin5 = min(c87620, _xlin4)
    _xlin9 = max(0., c05800 - (e07300 + c07180 + e07200 + _xlin5))
    _xlin10 = min(c87668, _xlin9)
    c87680 = _xlin5 + _xlin10
    c07230 = c87680
    _ctc1 = c07180 + e07200 + c07230
    _ctc2 = e07240 + e07960 + e07260 + e07300
    _regcrd = _ctc1 + _ctc2
    _exocrd = e07700 + e07250
    _exocrd = _exocrd + t07950
    _ctctax = c05800 - _regcrd - _exocrd
    c07220 = min(_precrd, max(0., _ctctax))
    # lt tax owed
    _avail = c05800
    c07180 = min(c07180, _avail)
    _avail = _avail - c07180
    c07200 = min(e07200, _avail)
    _avail = _avail - c07200
    c07300 = min(e07300, _avail)
    _avail = _avail - c07300
    c07230 = min(c07230, _avail)
    _avail = _avail - c07230
    c07240 = min(e07240, _avail)
    _avail = _avail - c07240
    c07260 = min(e07260, _avail)
    _avail = _avail - c07260
    c07250 = min(e07250, _avail)
    _avail = _avail - c07250
    c07600 = min(e07600, _avail)
    _avail = _avail - c07600
    c07220 = min(c07220, _avail)
    _avail = _avail - c07220
    # Allocate credits to tax in order on the tax form
    return (c87560, c87570, c87580, c87590, c87600, c87610, c07300, c07600,
            c07240, c87620, _ctc1, _ctc2, _regcrd, _exocrd, _ctctax, c07220,
            c07230, _avail)


@iterate_jit(nopython=True)
def AddCTC(_nctcr, _precrd, _earned, c07220, _fica_was,
           _exact, e82880, ACTC_Income_thd, ACTC_rt,
           ALD_SelfEmploymentTax_HC, e03260, e09800, c59660, e11200,
           e11070, e82915, e82940, ACTC_ChildNum):
    """
    AddCTC function: calculates Additional Child Tax Credit
    """
    c82925 = 0.
    c82930 = 0.
    c82935 = 0.
    c82880 = 0.
    c82885 = 0.
    c82890 = 0.
    c82900 = 0.
    c82905 = 0.
    c82910 = 0.
    c82915 = 0.
    c82920 = 0.
    c82937 = 0.
    c82940 = 0.
    c11070 = 0.
    _othadd = 0.
    # Part I of 2005 form 8812
    if _nctcr > 0:
        c82925 = _precrd
        c82930 = c07220
        c82935 = c82925 - c82930
        # CTC not applied to tax
        c82880 = max(0., _earned)
        if _exact == 1:
            c82880 = e82880
        c82885 = max(0., c82880 - ACTC_Income_thd)
        c82890 = ACTC_rt * c82885
    # Part II of 2005 form 8812
    if _nctcr >= ACTC_ChildNum and c82890 < c82935:
        c82900 = 0.5 * _fica_was
        c82905 = (1. - ALD_SelfEmploymentTax_HC) * e03260 + e09800
        c82910 = c82900 + c82905
        c82915 = c59660 + e11200
        c82920 = max(0., c82910 - c82915)
        c82937 = max(c82890, c82920)
    # Part II of 2005 form 8812
    if _nctcr > 0 and _nctcr <= 2 and c82890 > 0:
        c82940 = min(c82890, c82935)
    if _nctcr > 2:
        if c82890 >= c82935:
            c82940 = c82935
        else:
            c82940 = min(c82935, c82937)
    c11070 = c82940
    if e82915 > 0 and abs(e82940 - c82940) > 100:
        _othadd = e11070 - c11070
    return (c82925, c82930, c82935, c82880, c82885, c82890,
            c82900, c82905, c82910, c82915, c82920, c82937, c82940, c11070,
            _othadd)


def F5405(pol, rec):
    """
    F5405 function: Form 5405 First-Time Homebuyer Credit is not needed
    """
    if pol.current_year > 0:  # meaningless use of required first argument
        c64450 = np.zeros((rec.dim,))
    return pd.DataFrame(data=np.column_stack((c64450,)), columns=['c64450'])


@iterate_jit(nopython=True, puf=True)
def C1040(e07400, e07200, c07220, c07230, c07300, c07240,
          e07260, c07970, x07400, e09720, c07600,
          e07500, e07700, p08000, e08001, e07960,
          e07980, c05800, e08800, e09900, e09400, e09800,
          e10000, e10100, e09700, e10050, e10075, e09805, e09710,
          c07180, NIIT, puf):
    """
    C1040 function: ...
    """
    # Credits 1040 line 48
    x07400 = e07400
    c07100 = (c07180 + e07200 + c07600 + c07300 + x07400 + e07980 + c07220 +
              e07500 + p08000)
    y07100 = c07100
    c07100 += e07700 + c07230 + c07970 + c07240 + e07260 + e08001 + e07960
    x07100 = c07100
    c07100 = min(c07100, c05800)
    # Tax After credits 1040 line 52
    c08795 = max(0., c05800 - c07100)  # SAS @1277
    if puf:
        e08795 = e08800
    else:
        e08795 = 0.
    # Tax before refundable credits
    _othertax = e09900 + e09400 + e09800 + e10000 + e10100 + NIIT
    c09200 = _othertax + c08795
    # assuming year (FLPDYR) > 2009
    c09200 = c09200 + e09700 + e10050 + e10075 + e09805 + e09710 + e09720
    return (c07100, c07970, y07100, x07100, c08795, e08795, c09200, _othertax)


@iterate_jit(nopython=True)
def DEITC(c59660, c07100, c08800, c05800, _avail, e11601, e07170, _othertax):
    """
    DEITC function: decomposition of EITC
    """
    _comb = 0.
    c10950 = 0.
    c59680 = min(c59660, _avail)
    _avail = _avail - c59680
    _avail = max(0., _avail - e07170)
    _avail = _avail + _othertax
    c59700 = min(_avail, c59660 - c59680)
    c59720 = c59660 - c59680 - c59700
    c07150 = c07100 + c59680 + e11601
    c07150 = min(c07150, c05800)
    c08800 = c05800 - c07150
    return (c59680, c59700, c59720, _comb, c07150, c10950, c08800)


@iterate_jit(nopython=True)
def IITAX(c09200, c59660, c11070, c10960, c11600, c10950, _eitc, e11580,
          e11450, e11500, e82040, e11550, e10000, _fica, _personal_credit, n24,
          CTC_additional, CTC_additional_ps, CTC_additional_prt, c00100,
          _sep, MARS):
    """
    IITAX function: ...
    """
    _refund = (c59660 + c11070 + c10960 + c10950 + c11600 + e11580 + e11450 +
               e11500 + _personal_credit)
    _iitax = c09200 - _refund - e82040
    _combined = _iitax + _fica
    potential_add_CTC = max(0., min(_combined, CTC_additional * n24))
    phaseout = (c00100 -
                CTC_additional_ps[MARS - 1]) * (CTC_additional_prt / _sep)
    final_add_CTC = max(0., potential_add_CTC - max(0., phaseout))

    _iitax = _iitax - final_add_CTC
    # updated combined tax liabilities after applying the credit
    _combined = _iitax + _fica
    _refund = _refund + final_add_CTC
    _payments = (c59660 + c10950 + c10960 + c11070 + e10000 + e11550 +
                 e11450 + e11500)
    c10300 = max(0., c09200 - _payments)
    _eitc = c59660
    return (c10300, _eitc, _refund, _iitax, _combined)


@jit(nopython=True)
def Taxer_i(inc_in, MARS, II_rt1, II_rt2, II_rt3, II_rt4, II_rt5, II_rt6,
            II_rt7, II_brk1, II_brk2, II_brk3, II_brk4, II_brk5, II_brk6):
    """
    Taxer_i function: ...
    """
    _a6 = inc_in
    inc_out = (II_rt1 * min(_a6, II_brk1[MARS - 1]) + II_rt2 *
               min(II_brk2[MARS - 1] - II_brk1[MARS - 1],
                   max(0., _a6 - II_brk1[MARS - 1])) + II_rt3 *
               min(II_brk3[MARS - 1] - II_brk2[MARS - 1],
                   max(0., _a6 - II_brk2[MARS - 1])) + II_rt4 *
               min(II_brk4[MARS - 1] - II_brk3[MARS - 1],
                   max(0., _a6 - II_brk3[MARS - 1])) + II_rt5 *
               min(II_brk5[MARS - 1] - II_brk4[MARS - 1],
                   max(0., _a6 - II_brk4[MARS - 1])) + II_rt6 *
               min(II_brk6[MARS - 1] - II_brk5[MARS - 1],
                   max(0., _a6 - II_brk5[MARS - 1])) + II_rt7 *
               max(0., _a6 - II_brk6[MARS - 1]))
    return inc_out


@iterate_jit(nopython=True)
def ExpandIncome(_fica_was, e02400, c02500, c00100, e00400):
    """
    ExpandIncome function: ...
    """
    employer_share_fica = 0.5 * _fica_was
    non_taxable_ss_benefits = e02400 - c02500
    _expanded_income = (c00100 +  # AGI
                        e00400 +  # Non-taxable interest
                        non_taxable_ss_benefits +
                        employer_share_fica)
    return _expanded_income


def BenefitSurtax(calc):
    """
    BenefitSurtax function: ...
    """
    if calc.policy.ID_BenefitSurtax_crt != 1.:
        nobenefits_calc = copy.deepcopy(calc)
        # hard code the reform
        nobenefits_calc.policy.ID_Medical_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[0])
        nobenefits_calc.policy.ID_StateLocalTax_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[1])
        nobenefits_calc.policy.ID_RealEstate_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[2])
        nobenefits_calc.policy.ID_casualty_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[3])
        nobenefits_calc.policy.ID_Miscellaneous_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[4])
        nobenefits_calc.policy.ID_InterestPaid_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[5])
        nobenefits_calc.policy.ID_Charity_HC = \
            int(nobenefits_calc.policy.ID_BenefitSurtax_Switch[6])
        nobenefits_calc.calc_one_year()
        # pylint: disable=protected-access
        tax_diff = np.where(
            nobenefits_calc.records._iitax - calc.records._iitax > 0.,
            nobenefits_calc.records._iitax - calc.records._iitax,
            0.)
        surtax_cap = nobenefits_calc.policy.ID_BenefitSurtax_crt *\
            nobenefits_calc.records.c00100
        calc.records._surtax[:] = calc.policy.ID_BenefitSurtax_trt * np.where(
            tax_diff > surtax_cap, tax_diff - surtax_cap, 0.)
        calc.records._iitax += calc.records._surtax
        calc.records._combined = calc.records._iitax + calc.records._fica
