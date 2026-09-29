# Status

Run on 2026-09-28 with:

- scipy: release 1.18.1, development 2.0.0.dev0+git20260924.31619d9 (build nightly-20260926)
  (release: numpy 2.5.3, mpmath 1.4.1; development: numpy 2.6.0.dev0+git20260922.e29186c, mpmath 1.5.0a1)
- statsmodels: release 0.15.0, development 0.15.1.dev84+g15b987752 (build git-15b987752e)
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)
- networkx: release 3.7, development 3.7.1rc0.dev0 (build git-9f6079c012)
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)
- mne: release 1.13.2, development 1.14.0.dev48+gd7ffc6037 (build git-d7ffc6037c)
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)

| Script | Release | Development | Message (release) |
|---|---|---|---|
| `mne_f_mway_rm_greenhouse_geisser.py` | present | present | p = 0.005284954095414777, expected 0.004901544000240306 (epsilon 0.9251); F = 4.997235, independent F = 4.997235 (agree: True) |
| `mne_f_oneway_sigma_docstring.py` | present | present | F = 12.0; the documented formula gives 9.0; docstring wording present: True |
| `mne_fdr_correction_boundary.py` | present | present | reject=[True, False], p_adj=[0.02, 0.05]; expected reject=[True, True], p_adj=[0.02, 0.05] |
| `mne_permutation_cluster_1samp_adjacency_false.py` | present | not reproduced | clusters with adjacency=None: [(0,)]; with adjacency=False: [()] |
| `mne_permutation_cluster_1samp_all_not_exact.py` | present | present | cluster (0, 1, 2, 3): exact p from 512 classes = 0.00195312; seed 0: p = 0.00195695, len(H0) = 511, missing {0.0: 1}, extra {}; seed 1: p = 0.00195695, len(H0) = 511, missing {4.37 |
| `mne_permutation_cluster_1samp_all_seed_dependent.py` | present | present | cluster (0, 1): seed 0 p = 0.035225, seed 1 p = 0.035225, exact 0.035156; cluster (3,): seed 0 p = 0.763209, seed 1 p = 0.765166, exact 0.763672 |
| `mne_permutation_cluster_1samp_exact_one_tailed.py` | present | present | p = 0.03125 vs exact np.float64(0.015625); (observed, zeros) in H0 (2, 42), in the enumeration (1, 43) |
| `networkx_edge_current_flow_digraph_exception_docstring.py` | present | present | raised NetworkXNotImplemented (not implemented for directed type); subclass of NetworkXError: False; docstring documents NetworkXError for DiGraphs: True |
| `networkx_generate_random_paths_isolated.py` | present | present | raised ValueError: probabilities contain NaN |
| `networkx_group_betweenness_isolate.py` | present | present | group with node 5: 5.0; without node 5: 3.0; relabelled, with node 5: 3.0; brute force 3.0 |
| `networkx_group_betweenness_regression.py` | present | present | labels 6, 11, 2, 3: 0.5; relabelled 0 to 3: 0.0; brute force 0.0 |
| `networkx_group_degree_centrality_duplicates.py` | present | present | {'[1]': 0.5, '{1}': 0.5, '[1, 1]': 0.6666666666666666}; docstring accepts a list or set: True |
| `networkx_node_degree_xy_nodes_docstring.py` | present | present | got []; the documented behaviour gives [(1, 2), (1, 2), (2, 1), (2, 1)]; docstring wording present: True |
| `networkx_single_source_all_shortest_paths_zero_weight.py` | present | present | got {0: [[0], [0]], 1: [[0, 1]], 2: [[0, 1, 2]]}; expected {0: [[0]], 1: [[0, 1]], 2: [[0, 1, 2]]} |
| `scipy_barnard_exact_row_swap.py` | present | present | two-sided, pooled=False: 0.0055692 vs 0.0051505 after swapping rows |
| `scipy_barnard_exact_ties.py` | present | present | got 0.034076716; tail probability with the tie at pi = 0.6635: 0.034109155 (lower bound); maximum without the tied table: 0.034076716; float64 statistics: observed np.float64(-1.89 |
| `scipy_boxcox_normmax_pearsonr_ymax.py` | present | present | docstring says ymax is ignored for pearsonr: True; lambda without ymax 0.044469323600991546, with ymax=0.25 0.0 |
| `scipy_boxcox_normmax_ymax.py` | present | present | returned lambda -2.220e-16: max /transform/ 1.5923 > ymax 1.1816; boundary lambda -0.3953 meets the bound |
| `scipy_dlaplace_log_tails.py` | present | present | logcdf(-1000, a=1) = -inf (expected -1000.313262); logsf(1000, a=1) = -inf (expected -1001.313262) |
| `scipy_dlaplace_logpmf_large_k.py` | present | present | logpmf(-1000, a=1) = -inf, expected -1000.7719368329053 |
| `scipy_dlaplace_sf_far_tail.py` | present | present | sf(10, a=5) = 0.0, expected 1.2908835202659582e-24 |
| `scipy_hyperu_negative_a.py` | present | present | 10 of 10 points wrong; (a, x, scipy, mpmath) at b = 0: [(-0.5, 0.1, nan, 0.6827926540154777), (-0.5, 1.0, nan, 1.2003469347909477), (-1.5, 0.1, nan, -0.3654721946005413), (-1.5, 1. |
| `scipy_hyperu_negative_b_accuracy.py` | present | present | b = -4.7012, x = 6.9068; a=1.4836: scipy 0.021023729695125847, mpmath 0.02102372820602505, rel. error 7.1e-08; a=2.4836: scipy 0.0013681253957007213, mpmath 0.0013681253961172338,  |
| `scipy_itj0y0_accuracy.py` | present | present | absolute error above 1e-12 (or NaN) at 59 of 101 sampled points in [12, 37]; largest 4.1e-09 at x = 20.0 (value -0.1682, relative error 2.4e-08) |
| `scipy_itj0y0_j0_accuracy.py` | present | present | absolute error above 1e-12 (or NaN) at 55 of 101 sampled points in [12, 37]; largest 1.1e-09 at x = 19.75 (value 1.0150, relative error 1.1e-09) |
| `scipy_kstest_norm_args.py` | present | not reproduced | raised TypeError: ndtr() takes from 1 to 2 positional arguments but 3 were given; the callable form gives statistic 0.5, p 1.0 |
| `scipy_nctdtridf_roundtrip.py` | present | present | p = 0.9785864072356195; nctdtridf(p, nc, t) = 1e+100, CDF residual 2.5e-04 (df = 7.42072530317493 has residual 0) |
| `scipy_nctdtridf_small_df.py` | present | not reproduced | 12 of 128 inversions fail; first (df, nc, t, returned): [(0.3, -0.5, -1.5, -1e+100), (0.3, -0.5, -0.3, 1e+100), (0.3, -0.5, -0.4, 1e+100)] |
| `scipy_obl_rad2_small_x.py` | present | present | scaled Wronskian, which must be the same at every x: x=0.2: obl_rad2=-1.145e-320, (x^2+1) W=1.11906e-320; x=0.5: obl_rad2=-7.698e-321, (x^2+1) W=1.11906e-320; x=1.0: obl_rad2=-2.61 |
| `scipy_poisson_means_test_equal_rates.py` | present | present | pvalue = 0.8646647167633871, expected 1.0 |
| `scipy_pro_rad_wronskian.py` | present | present | scaled Wronskian, which must be the same at every x: x=1.1: 0.996076; x=1.2: 0.983038; x=1.5: 0.870417; x=2.0: 1.000000; x=4.0: 1.000000 |
| `scipy_skewtest_symmetric_sample.py` | present | present | statistic=1.0108048609177787 pvalue=0.3121098361421897; expected 0 and 1 |
| `scipy_spearmanr_omit_pvalue.py` | present | present | statistic=1.0000000000000002 pvalue=1.0; expected statistic 1 and pvalue 0 |
| `scipy_truncate_icdf_far_tail.py` | present | present | icdf(0.5) = inf, expected 10.06841183608143 |
| `scipy_truncate_pdf_at_bound.py` | present | present | truncated Normal at its bound: pdf 0.0, logpdf -inf; support (2.0, 8.0); truncnorm pdf 2.373215532822906; truncated Uniform pdf at its bound 0.1666666666666666 |
| `scipy_y1p_zeros_complex_docstring.py` | present | present | first complex zero 0.576785+0.903985j, /Y1'/ there 1e-16; docstring states negative real part: True |
| `scipy_y1p_zeros_real_accuracy.py` | present | present | relative errors of the first six real zeros: 0.0e+00, 5.6e-15, 7.4e-14, 1.4e-09, 2.7e-10, 6.8e-11 |
| `statsmodels_chisquare_effectsize_axis.py` | present | present | axis=1 raised ValueError: operands could not be broadcast together with shapes (3,4) (3,) ; axis=0 on the transposed input gives [0.0, 0.0, 0.0] |
| `statsmodels_chisquare_effectsize_axis1_values.py` | present | present | axis=1: [0.2916666666666667, 2.3333333333333335]; exact per-row effect sizes [0.3333333333333333, 1.3333333333333333]; axis=0 on the transposed input: [0.3333333333333333, 1.333333 |
| `statsmodels_confint_poisson_2indep_sqrtcc_exposure.py` | present | present | exposure2=10: (0.22451098663306185, 1.0565389600576878); exposure2=40: (0.22451098663306185, 1.0565389600576878); expected the second to be 4 times the first |
| `statsmodels_confint_poisson_midp_zero_count.py` | present | present | got (2.9957322769165073, 2.9957322735405425), expected (0, 2.995732273553991) |
| `statsmodels_confint_proportions_2indep_score_diff.py` | present | present | 12/35 vs 18/42: got (-0.287057, 0.133486), expected (-0.294436, 0.134119) |
| `statsmodels_confint_proportions_2indep_score_raise.py` | present | present | raised ValueError: The function value at x=-0.7749807427901235 is NaN; solver cannot continue. |
| `statsmodels_fdrcorrection_twostage_bool_maxiter.py` | present | present | corrected p with maxiter=False [0.06, 0.06, 0.06, 0.45, 1.0], maxiter=1 [0.024, 0.024, 0.024, 0.18, 0.432], maxiter=0 [0.06, 0.06, 0.06, 0.45, 1.0] |
| `statsmodels_fdrcorrection_twostage_maxiter_true.py` | present | present | corrected p with maxiter=True [0.024, 0.024, 0.024, 0.18, 0.432], maxiter=-1 [0.012, 0.012, 0.012, 0.09, 0.216], maxiter=1 [0.024, 0.024, 0.024, 0.18, 0.432] |
| `statsmodels_het_goldfeldquandt_df.py` | present | present | pvalue=0.0027834938934368355, expected 0.015219391272578164 (df1=10, df2=26) |
| `statsmodels_het_goldfeldquandt_df_decreasing.py` | present | present | pvalue=0.9972165061065632, expected 0.9847806087274218 (df1=10, df2=26) |
| `statsmodels_jonckheere_terpstra_fully_tied.py` | present | present | sizes (4, 4, 4): raised ValueError; sizes (5, 4, 6): returned p = 0.5 (var_null 8.881784197001252e-16) |
| `statsmodels_nonequivalence_poisson_2indep.py` | present | present | pvalue=1.284999345311911 |
| `statsmodels_nonequivalence_poisson_2indep_statistic.py` | present | present | statistic=4.746928831711439; one-sided tests: lower bound statistic 4.746928831711439 (p 1), upper bound statistic -0.365148371670111 (p 0.6425) |
| `statsmodels_runstest_2samp_continuity_correction.py` | present | present | runs 4, expectation 27/7; library z = 0.6836, p = 0.4942; SAS rule z = -0.3798, p = 0.7041 |
| `statsmodels_runstest_2samp_group_labels.py` | present | present | groups 0/1: (-1.1456439237389602, 0.2519425151568083); groups 1/2: (-inf, 0.0); groups 5/7: (nan, nan) |
| `statsmodels_runstest_2samp_integer_ties.py` | present | present | integer input raised UFuncTypeError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'; the same values as floats give (0.0, 1.0) |
| `statsmodels_runstest_continuity_correction.py` | present | present | runs 3, expectation 14/5; library z = 1.7500, p = 0.0801; SAS rule z = -0.7500, p = 0.4533 |
| `statsmodels_score_test_proportions_2indep_constrained_mle.py` | present | present | constrained estimate of p2 under p1 - p2 = 0.1: got 0.343763, expected 0.348098 |
| `statsmodels_transform_corr_normal_spearman.py` | present | present | return_var=True raised ValueError: The values in t must be monotonically increasing or monotonically decreasing; repeated values are allowed.; without return_var the result is [-0. |
| `statsmodels_tweedie_loglike_underflow.py` | present | present | got -inf, expected -1832.9551620564887 |
