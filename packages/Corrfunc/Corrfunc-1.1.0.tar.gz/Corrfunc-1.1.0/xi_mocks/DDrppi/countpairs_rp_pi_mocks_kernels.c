/* File: countpairs_rp_pi_mocks_kernels.c */
/*
  This file is a part of the Corrfunc package
  Copyright (C) 2015-- Manodeep Sinha (manodeep@gmail.com)
  License: MIT LICENSE. See LICENSE file under the top-level
  directory at https://github.com/manodeep/Corrfunc/
*/


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <stdint.h>
#include <inttypes.h>

#include "defs.h"
#include "utils.h"
#include "function_precision.h"


#if defined(USE_AVX) && defined(__AVX__)
#include "avx_calls.h"

static inline void countpairs_rp_pi_mocks_avx_intrinsics(DOUBLE *x0, DOUBLE *y0, DOUBLE *z0, DOUBLE *d0, const int64_t N0,
                                                         DOUBLE *x1, DOUBLE *y1, DOUBLE *z1, DOUBLE *d1, const int64_t N1, const int same_cell, 
                                                         const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const int npibin, const DOUBLE *rupp_sqr, const DOUBLE pimax
#ifdef PERIODIC                                             
                                                         ,const DOUBLE off_xwrap, const DOUBLE off_ywrap, const DOUBLE off_zwrap
#endif                                             
                                                         ,const AVX_FLOATS *m_rupp_sqr
                                                         
                                                         ,const AVX_FLOATS *m_kbin
#ifdef OUTPUT_RPAVG                                                   
                                                         ,DOUBLE *src_rpavg
#endif                         
                                                         ,uint64_t *src_npairs)
{
  const int64_t totnbins = (npibin+1)*(nbin+1);
  const DOUBLE sqr_max_sep = sqr_rpmax + pimax*pimax;
  const DOUBLE sqr_pimax = pimax*pimax;

  uint64_t *npairs = my_calloc(sizeof(*npairs), totnbins);
  const DOUBLE dpi = pimax/npibin;
  const DOUBLE inv_dpi = 1.0/dpi;
#ifdef OUTPUT_RPAVG
  DOUBLE rpavg[totnbins];
  for(int i=0;i<totnbins;i++) {
    rpavg[i] = ZERO;
  }
#endif

  for(int64_t i=0;i<N0;i++) {
    const DOUBLE xpos = *x0++;
    const DOUBLE ypos = *y0++;
    const DOUBLE zpos = *z0++;
    const DOUBLE dpos = *d0++;
    
    int64_t j = (same_cell == 1) ? (i+1):0;
    if(same_cell == 0) {
        DOUBLE *locald1 = d1;
        while(j < N1) {
            const DOUBLE dz = *locald1++ - dpos;
            if(dz > -pimax) break;
            j++;
        }
    }
    DOUBLE *localx1 = x1 + j;
    DOUBLE *localy1 = y1 + j;
    DOUBLE *localz1 = z1 + j;
    
    AVX_FLOATS m_xpos    = AVX_SET_FLOAT(xpos);
    AVX_FLOATS m_ypos    = AVX_SET_FLOAT(ypos);
    AVX_FLOATS m_zpos    = AVX_SET_FLOAT(zpos);
    union int8 {
        AVX_INTS m_ibin;
        int ibin[AVX_NVEC];
    };
    
                
#ifdef OUTPUT_RPAVG
    union float8{
        AVX_FLOATS m_Dperp;
        DOUBLE Dperp[AVX_NVEC];
    };
                
#endif
    
    const AVX_FLOATS m_sqr_pimax  = AVX_SET_FLOAT(sqr_pimax);
    const AVX_FLOATS m_sqr_rpmax  = AVX_SET_FLOAT(sqr_rpmax);
    const AVX_FLOATS m_max_sep = AVX_SET_FLOAT(sqr_max_sep);
    const AVX_FLOATS m_inv_dpi    = AVX_SET_FLOAT(inv_dpi);
    const AVX_FLOATS m_sqr_rpmin  = AVX_SET_FLOAT(sqr_rpmin);
    const AVX_FLOATS m_npibin     = AVX_SET_FLOAT((DOUBLE) npibin);
    const AVX_FLOATS m_zero       = AVX_SET_FLOAT(ZERO);
    const AVX_FLOATS m_one    = AVX_SET_FLOAT((DOUBLE) 1);
    
    for(;j<=(N1-AVX_NVEC);j+=AVX_NVEC){
        const AVX_FLOATS m_x2 = AVX_LOAD_FLOATS_UNALIGNED(localx1);
        const AVX_FLOATS m_y2 = AVX_LOAD_FLOATS_UNALIGNED(localy1);
        const AVX_FLOATS m_z2 = AVX_LOAD_FLOATS_UNALIGNED(localz1);
                    
        localx1 += AVX_NVEC;
        localy1 += AVX_NVEC;
        localz1 += AVX_NVEC;
                    
        AVX_FLOATS m_sqr_Dpar, m_sqr_Dperp;
        {
            const AVX_FLOATS m_parx = AVX_ADD_FLOATS(m_x2, m_xpos);
            const AVX_FLOATS m_pary = AVX_ADD_FLOATS(m_y2, m_ypos);
            const AVX_FLOATS m_parz = AVX_ADD_FLOATS(m_z2, m_zpos);
            
            const AVX_FLOATS m_perpx = AVX_SUBTRACT_FLOATS(m_xpos, m_x2);
            const AVX_FLOATS m_perpy = AVX_SUBTRACT_FLOATS(m_ypos, m_y2);
            const AVX_FLOATS m_perpz = AVX_SUBTRACT_FLOATS(m_zpos, m_z2);
            
            const AVX_FLOATS m_term1 = AVX_MULTIPLY_FLOATS(m_parx, m_perpx);
            const AVX_FLOATS m_term2 = AVX_MULTIPLY_FLOATS(m_pary, m_perpy);
            const AVX_FLOATS m_term3 = AVX_MULTIPLY_FLOATS(m_parz, m_perpz);
            const AVX_FLOATS m_numerator = AVX_SQUARE_FLOAT(AVX_ADD_FLOATS(m_term1, AVX_ADD_FLOATS(m_term2, m_term3)));
            
            const AVX_FLOATS m_sqr_perpx = AVX_SQUARE_FLOAT(m_perpx);
            const AVX_FLOATS m_sqr_perpy = AVX_SQUARE_FLOAT(m_perpy);
            const AVX_FLOATS m_sqr_perpz = AVX_SQUARE_FLOAT(m_perpz);
            const AVX_FLOATS m_sqr_sep = AVX_ADD_FLOATS(m_sqr_perpx, AVX_ADD_FLOATS(m_sqr_perpy, m_sqr_perpz));//3-d separation
            //The 3-d separation (| s.s |)^2 *must* be less than (pimax^2 + rpmax^2). If not, one of the
            //constraints for counting the pair (i.e., rp < rpmax, \pi < pimax) must be violated and
            //we would discard the pair.
            const AVX_FLOATS m_mask_3d_sep = AVX_COMPARE_FLOATS(m_sqr_sep, m_max_sep, _CMP_LT_OQ);
            
            const AVX_FLOATS m_sqr_norm_l = AVX_ADD_FLOATS(AVX_SQUARE_FLOAT(m_parx), AVX_ADD_FLOATS(AVX_SQUARE_FLOAT(m_pary), AVX_SQUARE_FLOAT(m_parz)));
            
            //\pi ^2 = |s.l| ^2 / |l|^2
            //However, division is slow -> so we will check if \pimax^2 * |l| ^2 < |s.l|^2. If not, then the
            //value of \pi (after division) *must* be larger than \pimax -> in which case we would
            //not count that pair anway.
            const AVX_FLOATS m_sqr_pimax_times_l = AVX_MULTIPLY_FLOATS(m_sqr_pimax, m_sqr_norm_l);
            const AVX_FLOATS m_mask_pimax_sep = AVX_COMPARE_FLOATS(m_numerator, m_sqr_pimax_times_l, _CMP_LT_OQ);// is pi < pimax ?
            //If the bits are all 0, then *none* of the pairs satisfy the pimax + rpmax constraints.
            const AVX_FLOATS m_mask = AVX_BITWISE_AND(m_mask_3d_sep, m_mask_pimax_sep);
            if(AVX_TEST_COMPARISON(m_mask)==0) {
                continue;
            }
            
#ifndef FAST_DIVIDE
            m_sqr_Dpar = AVX_DIVIDE_FLOATS(m_numerator,m_sqr_norm_l);
            //The divide is the actual operation we need
            // but divides are about 10x slower than multiplies. So, I am replacing it
            //with a approximate reciprocal in floating point
            // + 2 iterations of newton-raphson in case of DOUBLE
#else //following blocks do an approximate reciprocal followed by two iterations of Newton-Raphson

#ifndef DOUBLE_PREC
            //Taken from Intel's site: https://software.intel.com/en-us/articles/wiener-filtering-using-intel-advanced-vector-extensions
            // (which has bugs in it, just FYI). Plus, https://techblog.lankes.org/2014/06/16/avx-isnt-always-faster-then-see/
            __m256 rc  = _mm256_rcp_ps(m_sqr_norm_l);
#else
            //we have to do this for doubles now.
            //if the vrcpps instruction is not generated, there will
            //be a ~70 cycle performance hit from switching between
            //AVX and SSE modes.
            __m128 float_tmp1 =  _mm256_cvtpd_ps(m_sqr_norm_l);
            __m128 float_inv_tmp1 = _mm_rcp_ps(float_tmp1);
            AVX_FLOATS rc = _mm256_cvtps_pd(float_inv_tmp1);
#endif//DOUBLE_PREC
            
            //We have the double->float->approx. reciprocal->double process done.
            //Now improve the accuracy of the divide with newton-raphson.
            
            //Ist iteration of NewtonRaphson
            AVX_FLOATS two = AVX_SET_FLOAT((DOUBLE) 2.0);
            AVX_FLOATS rc1 = AVX_MULTIPLY_FLOATS(rc,
                                           AVX_SUBTRACT_FLOATS(two,
                                                         AVX_MULTIPLY_FLOATS(m_sqr_norm_l,rc)));
            //2nd iteration of NewtonRaphson
            AVX_FLOATS rc2 = AVX_MULTIPLY_FLOATS(rc1,
                                           AVX_SUBTRACT_FLOATS(two,
                                                         AVX_MULTIPLY_FLOATS(m_sqr_norm_l,rc1)));
            m_sqr_Dpar = AVX_MULTIPLY_FLOATS(m_numerator,rc2);
#endif//FAST_DIVIDE
            
            m_sqr_Dperp = AVX_SUBTRACT_FLOATS(m_sqr_sep,m_sqr_Dpar);
        }
        
        
        AVX_FLOATS m_mask_left;
        //Do the mask filters in a separate scope
        {
            const AVX_FLOATS m_mask_pimax = AVX_COMPARE_FLOATS(m_sqr_Dpar,m_sqr_pimax,_CMP_LT_OQ);
            if(AVX_TEST_COMPARISON(m_mask_pimax)==0) {
                j = N1;
                break;
            }
            const AVX_FLOATS m_rpmax_mask = AVX_COMPARE_FLOATS(m_sqr_Dperp, m_sqr_rpmax, _CMP_LT_OQ);
            const AVX_FLOATS m_rpmin_mask = AVX_COMPARE_FLOATS(m_sqr_Dperp, m_sqr_rpmin, _CMP_GE_OQ);
            const AVX_FLOATS m_rp_mask = AVX_BITWISE_AND(m_rpmax_mask,m_rpmin_mask);
            
            m_mask_left = AVX_BITWISE_AND(m_mask_pimax, m_rp_mask);
            if(AVX_TEST_COMPARISON(m_mask_left)==0) {
                continue;
            }
            
            m_sqr_Dperp = AVX_BLEND_FLOATS_WITH_MASK(m_zero,m_sqr_Dperp,m_mask_left);
            m_sqr_Dpar  = AVX_BLEND_FLOATS_WITH_MASK(m_sqr_pimax,m_sqr_Dpar,m_mask_left);
        }
        const AVX_FLOATS m_Dpar = AVX_SQRT_FLOAT(m_sqr_Dpar);
        
#ifdef OUTPUT_RPAVG
        union float8 union_mDperp;
        union_mDperp.m_Dperp = AVX_BLEND_FLOATS_WITH_MASK(m_zero,AVX_SQRT_FLOAT(m_sqr_Dperp),m_mask_left);
#endif
        const AVX_FLOATS m_mask = m_mask_left;
        AVX_FLOATS m_rpbin = AVX_SET_FLOAT((DOUBLE) 0);
        for(int kbin=nbin-1;kbin>=1;kbin--) {
            const AVX_FLOATS m_mask_low = AVX_COMPARE_FLOATS(m_sqr_Dperp,m_rupp_sqr[kbin-1],_CMP_GE_OQ);
            const AVX_FLOATS m_bin_mask = AVX_BITWISE_AND(m_mask_low,m_mask_left);
            m_rpbin = AVX_BLEND_FLOATS_WITH_MASK(m_rpbin,m_kbin[kbin], m_bin_mask);
            m_mask_left = AVX_COMPARE_FLOATS(m_sqr_Dperp, m_rupp_sqr[kbin-1],_CMP_LT_OQ);
            if(AVX_TEST_COMPARISON(m_mask_left) == 0) {
                break;
            }
        }
        
        /* Compute the 1-D index to the [rpbin, pibin] := rpbin*(npibin+1) + pibin */
        /*                      const AVX_FLOATS m_Dpar = AVX_SQRT_FLOAT(m_sqr_Dpar); */
        const AVX_FLOATS m_tmp2 = AVX_MULTIPLY_FLOATS(m_Dpar,m_inv_dpi);
        const AVX_FLOATS m_pibin = AVX_BLEND_FLOATS_WITH_MASK(m_npibin, m_tmp2, m_mask);
        const AVX_FLOATS m_npibin_p1 = AVX_ADD_FLOATS(m_npibin,m_one);
        const AVX_FLOATS m_binproduct = AVX_ADD_FLOATS(AVX_MULTIPLY_FLOATS(m_rpbin,m_npibin_p1),m_pibin);
        union int8 union_finalbin;
        union_finalbin.m_ibin = AVX_TRUNCATE_FLOAT_TO_INT(m_binproduct);
        
#if  __INTEL_COMPILER
#pragma unroll(AVX_NVEC)
#endif
        for(int jj=0;jj<AVX_NVEC;jj++) {
            const int ibin=union_finalbin.ibin[jj];
            
            npairs[ibin]++;
#ifdef OUTPUT_RPAVG
            rpavg [ibin] += union_mDperp.Dperp[jj];
#endif
            /* fprintf(stderr,"i=%d j=%d union_rpbin.ibin[jj] = %d union_pibin.ibin[jj] = %d\n",i,j,union_rpbin.ibin[jj],union_pibin.ibin[jj]); */
        }
    }//AVX j loop
    
    //Take care of the remainder
    for(;j<N1;j++) {
        const DOUBLE parx = xpos + *localx1;
        const DOUBLE pary = ypos + *localy1;
        const DOUBLE parz = zpos + *localz1;
        
        const DOUBLE perpx = xpos - *localx1;
        const DOUBLE perpy = ypos - *localy1;
        const DOUBLE perpz = zpos - *localz1;
        
        localx1++;localy1++;localz1++;
        
        const DOUBLE sqr_s = perpx*perpx + perpy*perpy + perpz*perpz;
        if(sqr_s >= sqr_max_sep) continue;
        
        const DOUBLE tmp  = (parx*perpx+pary*perpy+parz*perpz);
        const DOUBLE tmp1 = (parx*parx+pary*pary+parz*parz);
        const DOUBLE sqr_Dpar = (tmp*tmp)/tmp1;
        if(sqr_Dpar >= sqr_pimax) continue;
        
        const int pibin  = (sqr_Dpar >= sqr_pimax) ? npibin:(int) (SQRT(sqr_Dpar)*inv_dpi);
        const DOUBLE sqr_Dperp  = sqr_s - sqr_Dpar;
        if(sqr_Dperp >= sqr_rpmax || sqr_Dperp < sqr_rpmin) continue;
#ifdef OUTPUT_RPAVG
        const DOUBLE rp = SQRT(sqr_Dperp);
#endif
        for(int kbin=nbin-1;kbin>=1;kbin--) {
            if(sqr_Dperp >= rupp_sqr[kbin-1]) {
                const int ibin = kbin*(npibin+1) + pibin;
                npairs[ibin]++;
#ifdef OUTPUT_RPAVG
                rpavg[ibin]+=rp;
#endif
                break;
            }
        }
    }//remainder jloop
  }//i-loop

	for(int i=0;i<totnbins;i++) {
		src_npairs[i] += npairs[i];
#ifdef OUTPUT_RPAVG
        src_rpavg[i] += rpavg[i];
#endif        
        
	}
	free(npairs);
}
#endif //AVX defined and USE_AVX




#if defined(__SSE4_2__)
#include "sse_calls.h"

static inline void countpairs_rp_pi_mocks_sse_intrinsics(DOUBLE *x0, DOUBLE *y0, DOUBLE *z0, DOUBLE *d0, const int64_t N0,
                                                         DOUBLE *x1, DOUBLE *y1, DOUBLE *z1, DOUBLE *d1, const int64_t N1, const int same_cell, 
                                                         const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const int npibin, const DOUBLE *rupp_sqr, const DOUBLE pimax
#ifdef PERIODIC                                             
                                                         ,const DOUBLE off_xwrap, const DOUBLE off_ywrap, const DOUBLE off_zwrap
#endif                                             
                                                         ,const SSE_FLOATS *m_rupp_sqr
                                                         
                                                         ,const SSE_FLOATS *m_kbin
#ifdef OUTPUT_RPAVG                                                   
                                                         ,DOUBLE *src_rpavg
#endif                         
                                                         ,uint64_t *src_npairs)
{
  const int64_t totnbins = (npibin+1)*(nbin+1);
  const DOUBLE sqr_max_sep = sqr_rpmax + pimax*pimax;
  const DOUBLE sqr_pimax = pimax*pimax;

  uint64_t *npairs = my_calloc(sizeof(*npairs), totnbins);
  const DOUBLE dpi = pimax/npibin;
  const DOUBLE inv_dpi = 1.0/dpi;
#ifdef OUTPUT_RPAVG
  DOUBLE rpavg[totnbins];
  for(int i=0;i<totnbins;i++) {
    rpavg[i] = ZERO;
  }
#endif

  for(int64_t i=0;i<N0;i++) {
    const DOUBLE xpos = *x0++;
    const DOUBLE ypos = *y0++;
    const DOUBLE zpos = *z0++;
    const DOUBLE dpos = *d0++;
    
    int64_t j = (same_cell == 1) ? (i+1):0;
    if(same_cell == 0) {
        DOUBLE *locald1 = d1;
        while(j < N1) {
            const DOUBLE dz = *locald1++ - dpos;
            if(dz > -pimax) break;
            j++;
        }
    }
    DOUBLE *localx1 = x1 + j;
    DOUBLE *localy1 = y1 + j;
    DOUBLE *localz1 = z1 + j;
    
    SSE_FLOATS m_xpos    = SSE_SET_FLOAT(xpos);
    SSE_FLOATS m_ypos    = SSE_SET_FLOAT(ypos);
    SSE_FLOATS m_zpos    = SSE_SET_FLOAT(zpos);
    union int8 {
        SSE_INTS m_ibin;
        int ibin[SSE_NVEC];
    };
    
                
#ifdef OUTPUT_RPAVG
    union float8{
        SSE_FLOATS m_Dperp;
        DOUBLE Dperp[SSE_NVEC];
    };
                
#endif
    
    const SSE_FLOATS m_sqr_pimax  = SSE_SET_FLOAT(sqr_pimax);
    const SSE_FLOATS m_sqr_rpmax  = SSE_SET_FLOAT(sqr_rpmax);
    const SSE_FLOATS m_max_sep = SSE_SET_FLOAT(sqr_max_sep);
    const SSE_FLOATS m_inv_dpi    = SSE_SET_FLOAT(inv_dpi);
    const SSE_FLOATS m_sqr_rpmin  = SSE_SET_FLOAT(sqr_rpmin);
    const SSE_FLOATS m_npibin     = SSE_SET_FLOAT((DOUBLE) npibin);
    const SSE_FLOATS m_zero       = SSE_SET_FLOAT(ZERO);
    const SSE_FLOATS m_one    = SSE_SET_FLOAT((DOUBLE) 1);
    
    for(;j<=(N1-SSE_NVEC);j+=SSE_NVEC){
        const SSE_FLOATS m_x2 = SSE_LOAD_FLOATS_UNALIGNED(localx1);
        const SSE_FLOATS m_y2 = SSE_LOAD_FLOATS_UNALIGNED(localy1);
        const SSE_FLOATS m_z2 = SSE_LOAD_FLOATS_UNALIGNED(localz1);
                    
        localx1 += SSE_NVEC;
        localy1 += SSE_NVEC;
        localz1 += SSE_NVEC;
                    
        SSE_FLOATS m_sqr_Dpar, m_sqr_Dperp;
        {
            const SSE_FLOATS m_parx = SSE_ADD_FLOATS(m_x2, m_xpos);
            const SSE_FLOATS m_pary = SSE_ADD_FLOATS(m_y2, m_ypos);
            const SSE_FLOATS m_parz = SSE_ADD_FLOATS(m_z2, m_zpos);
            
            const SSE_FLOATS m_perpx = SSE_SUBTRACT_FLOATS(m_xpos, m_x2);
            const SSE_FLOATS m_perpy = SSE_SUBTRACT_FLOATS(m_ypos, m_y2);
            const SSE_FLOATS m_perpz = SSE_SUBTRACT_FLOATS(m_zpos, m_z2);
            
            const SSE_FLOATS m_term1 = SSE_MULTIPLY_FLOATS(m_parx, m_perpx);
            const SSE_FLOATS m_term2 = SSE_MULTIPLY_FLOATS(m_pary, m_perpy);
            const SSE_FLOATS m_term3 = SSE_MULTIPLY_FLOATS(m_parz, m_perpz);
            const SSE_FLOATS m_numerator = SSE_SQUARE_FLOAT(SSE_ADD_FLOATS(m_term1, SSE_ADD_FLOATS(m_term2, m_term3)));
            
            const SSE_FLOATS m_sqr_perpx = SSE_SQUARE_FLOAT(m_perpx);
            const SSE_FLOATS m_sqr_perpy = SSE_SQUARE_FLOAT(m_perpy);
            const SSE_FLOATS m_sqr_perpz = SSE_SQUARE_FLOAT(m_perpz);
            const SSE_FLOATS m_sqr_sep = SSE_ADD_FLOATS(m_sqr_perpx, SSE_ADD_FLOATS(m_sqr_perpy, m_sqr_perpz));//3-d separation
            //The 3-d separation (| s.s |)^2 *must* be less than (pimax^2 + rpmax^2). If not, one of the
            //constraints for counting the pair (i.e., rp < rpmax, \pi < pimax) must be violated and
            //we would discard the pair.
            const SSE_FLOATS m_mask_3d_sep = SSE_COMPARE_FLOATS_LT(m_sqr_sep, m_max_sep);
            
            const SSE_FLOATS m_sqr_norm_l = SSE_ADD_FLOATS(SSE_SQUARE_FLOAT(m_parx), SSE_ADD_FLOATS(SSE_SQUARE_FLOAT(m_pary), SSE_SQUARE_FLOAT(m_parz)));
            
            //\pi ^2 = |s.l| ^2 / |l|^2
            //However, division is slow -> so we will check if \pimax^2 * |l| ^2 < |s.l|^2. If not, then the
            //value of \pi (after division) *must* be larger than \pimax -> in which case we would
            //not count that pair anway.
            const SSE_FLOATS m_sqr_pimax_times_l = SSE_MULTIPLY_FLOATS(m_sqr_pimax, m_sqr_norm_l);
            const SSE_FLOATS m_mask_pimax_sep = SSE_COMPARE_FLOATS_LT(m_numerator, m_sqr_pimax_times_l);// is pi < pimax ?
            //If the bits are all 0, then *none* of the pairs satisfy the pimax + rpmax constraints.
            const SSE_FLOATS m_mask = SSE_BITWISE_AND(m_mask_3d_sep, m_mask_pimax_sep);
            if(SSE_TEST_COMPARISON(m_mask)==0) {
                continue;
            }
            
#ifndef FAST_DIVIDE
            m_sqr_Dpar = SSE_DIVIDE_FLOATS(m_numerator,m_sqr_norm_l);
            //The divide is the actual operation we need
            // but divides are about 10x slower than multiplies. So, I am replacing it
            //with a approximate reciprocal in floating point
            // + 2 iterations of newton-raphson in case of DOUBLE
#else //following blocks do an approximate reciprocal followed by two iterations of Newton-Raphson
#error not implemented for SSE

#ifndef DOUBLE_PREC
            //Taken from Intel's site: https://software.intel.com/en-us/articles/wiener-filtering-using-intel-advanced-vector-extensions
            // (which has bugs in it, just FYI). Plus, https://techblog.lankes.org/2014/06/16/avx-isnt-always-faster-then-see/
            __m256 rc  = _mm256_rcp_ps(m_sqr_norm_l);
            __m256 two = SSE_SET_FLOAT(2.0f);
            __m256 rc1 = _mm256_mul_ps(rc,
                                       _mm256_sub_ps(two,
                                                     _mm256_mul_ps(m_sqr_norm_l,rc)));
            
            __m256 rc2 = _mm256_mul_ps(rc1,
                                       _mm256_sub_ps(two,
                                                     _mm256_mul_ps(m_sqr_norm_l,rc1)));
            
            m_sqr_Dpar = _mm256_mul_ps ( m_numerator , rc2 );
            
#else
            //we have to do this for doubles now.
            //if the vrcpps instruction is not generated, there will
            //be a ~70 cycle performance hit from switching between
            //SSE and SSE modes.
            __m128 float_tmp1 =  _mm256_cvtpd_ps(m_sqr_norm_l);
            __m128 float_inv_tmp1 = _mm_rcp_ps(float_tmp1);
            SSE_FLOATS rc = _mm256_cvtps_pd(float_inv_tmp1);
            
            //We have the double->float->approx. reciprocal->double process done.
            //Now improve the accuracy of the divide with newton-raphson.
            
            //Ist iteration of NewtonRaphson
            SSE_FLOATS two = SSE_SET_FLOAT(2.0);
            SSE_FLOATS rc1 = _mm256_mul_pd(rc,
                                           _mm256_sub_pd(two,
                                                         _mm256_mul_pd(m_sqr_norm_l,rc)));
            //2nd iteration of NewtonRaphson
            SSE_FLOATS rc2 = _mm256_mul_pd(rc1,
                                           _mm256_sub_pd(two,
                                                         _mm256_mul_pd(m_sqr_norm_l,rc1)));
            m_sqr_Dpar = SSE_MULTIPLY_FLOATS(m_numerator,rc2);
#endif//DOUBLE_PREC
            
            
#endif//FAST_DIVIDE
            
            m_sqr_Dperp = SSE_SUBTRACT_FLOATS(m_sqr_sep,m_sqr_Dpar);
        }
        
        
        const SSE_FLOATS m_Dpar = SSE_SQRT_FLOAT(m_sqr_Dpar);
        
        SSE_FLOATS m_mask_left;
        //Do the mask filters in a separate scope
        {
            const SSE_FLOATS m_mask_pimax = SSE_COMPARE_FLOATS_LT(m_sqr_Dpar,m_sqr_pimax);
            const SSE_FLOATS m_rpmax_mask = SSE_COMPARE_FLOATS_LT(m_sqr_Dperp, m_sqr_rpmax);
            const SSE_FLOATS m_rpmin_mask = SSE_COMPARE_FLOATS_GE(m_sqr_Dperp, m_sqr_rpmin);
            const SSE_FLOATS m_rp_mask = SSE_BITWISE_AND(m_rpmax_mask,m_rpmin_mask);
            
            m_mask_left = SSE_BITWISE_AND(m_mask_pimax, m_rp_mask);
            if(SSE_TEST_COMPARISON(m_mask_left)==0) {
                continue;
            }
            
            m_sqr_Dperp = SSE_BLEND_FLOATS_WITH_MASK(m_zero,m_sqr_Dperp,m_mask_left);
            m_sqr_Dpar  = SSE_BLEND_FLOATS_WITH_MASK(m_sqr_pimax,m_sqr_Dpar,m_mask_left);
        }
#ifdef OUTPUT_RPAVG
        union float8 union_mDperp;
        union_mDperp.m_Dperp = SSE_BLEND_FLOATS_WITH_MASK(m_zero,SSE_SQRT_FLOAT(m_sqr_Dperp),m_mask_left);
#endif
        const SSE_FLOATS m_mask = m_mask_left;
        SSE_FLOATS m_rpbin = SSE_SET_FLOAT((DOUBLE) 0);
        for(int kbin=nbin-1;kbin>=1;kbin--) {
            const SSE_FLOATS m_mask_low = SSE_COMPARE_FLOATS_GE(m_sqr_Dperp,m_rupp_sqr[kbin-1]);
            const SSE_FLOATS m_bin_mask = SSE_BITWISE_AND(m_mask_low,m_mask_left);
            m_rpbin = SSE_BLEND_FLOATS_WITH_MASK(m_rpbin,m_kbin[kbin], m_bin_mask);
            m_mask_left = SSE_COMPARE_FLOATS_LT(m_sqr_Dperp, m_rupp_sqr[kbin-1]);
            if(SSE_TEST_COMPARISON(m_mask_left) == 0) {
                break;
            }
        }
        
        /* Compute the 1-D index to the [rpbin, pibin] := rpbin*(npibin+1) + pibin */
        /*                      const SSE_FLOATS m_Dpar = SSE_SQRT_FLOAT(m_sqr_Dpar); */
        const SSE_FLOATS m_tmp2 = SSE_MULTIPLY_FLOATS(m_Dpar,m_inv_dpi);
        const SSE_FLOATS m_pibin = SSE_BLEND_FLOATS_WITH_MASK(m_npibin, m_tmp2, m_mask);
        const SSE_FLOATS m_npibin_p1 = SSE_ADD_FLOATS(m_npibin,m_one);
        const SSE_FLOATS m_binproduct = SSE_ADD_FLOATS(SSE_MULTIPLY_FLOATS(m_rpbin,m_npibin_p1),m_pibin);
        union int8 union_finalbin;
        union_finalbin.m_ibin = SSE_TRUNCATE_FLOAT_TO_INT(m_binproduct);
        
#if  __INTEL_COMPILER
#pragma unroll(NVEC)
#endif
        for(int jj=0;jj<NVEC;jj++) {
            const int ibin=union_finalbin.ibin[jj];
            
            npairs[ibin]++;
#ifdef OUTPUT_RPAVG
            rpavg [ibin] += union_mDperp.Dperp[jj];
#endif
            /* fprintf(stderr,"i=%d j=%d union_rpbin.ibin[jj] = %d union_pibin.ibin[jj] = %d\n",i,j,union_rpbin.ibin[jj],union_pibin.ibin[jj]); */
        }
    }//SSE j loop
    
    //Take care of the remainder
    for(;j<N1;j++) {
        const DOUBLE parx = xpos + *localx1;
        const DOUBLE pary = ypos + *localy1;
        const DOUBLE parz = zpos + *localz1;
        
        const DOUBLE perpx = xpos - *localx1;
        const DOUBLE perpy = ypos - *localy1;
        const DOUBLE perpz = zpos - *localz1;
        
        localx1++;localy1++;localz1++;
        
        const DOUBLE sqr_s = perpx*perpx + perpy*perpy + perpz*perpz;
        if(sqr_s >= sqr_max_sep) continue;
        
        const DOUBLE tmp  = (parx*perpx+pary*perpy+parz*perpz);
        const DOUBLE tmp1 = (parx*parx+pary*pary+parz*parz);
        const DOUBLE sqr_Dpar = (tmp*tmp)/tmp1;
        if(sqr_Dpar >= sqr_pimax) continue;
        
        const int pibin  = (sqr_Dpar >= sqr_pimax) ? npibin:(int) (SQRT(sqr_Dpar)*inv_dpi);
        const DOUBLE sqr_Dperp  = sqr_s - sqr_Dpar;
        if(sqr_Dperp >= sqr_rpmax || sqr_Dperp < sqr_rpmin) continue;
#ifdef OUTPUT_RPAVG
        const DOUBLE rp = SQRT(sqr_Dperp);
#endif
        for(int kbin=nbin-1;kbin>=1;kbin--) {
            if(sqr_Dperp >= rupp_sqr[kbin-1]) {
                const int ibin = kbin*(npibin+1) + pibin;
                npairs[ibin]++;
#ifdef OUTPUT_RPAVG
                rpavg[ibin]+=rp;
#endif
                break;
            }
        }
    }//remainder jloop
  }//i-loop

	for(int i=0;i<totnbins;i++) {
		src_npairs[i] += npairs[i];
#ifdef OUTPUT_RPAVG
    src_rpavg[i] += rpavg[i];
#endif        
        
	}
	free(npairs);
}
#endif //SSE4.2 defined 


static inline void countpairs_rp_pi_mocks_naive(DOUBLE *x0, DOUBLE *y0, DOUBLE *z0, DOUBLE *d0, const int64_t N0,
                                                DOUBLE *x1, DOUBLE *y1, DOUBLE *z1, DOUBLE *d1, const int64_t N1, const int same_cell, 
                                                const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const int npibin, const DOUBLE *rupp_sqr, const DOUBLE pimax
#ifdef OUTPUT_RPAVG                                                   
                                                ,DOUBLE *src_rpavg
#endif                         
                                                ,uint64_t *src_npairs)
{

    /*----------------- FALLBACK CODE --------------------*/
    const int64_t totnbins = (npibin+1)*(nbin+1);
    const DOUBLE sqr_max_sep = sqr_rpmax + pimax*pimax;
    const DOUBLE sqr_pimax = pimax*pimax;

    uint64_t npairs[totnbins];
    for(int i=0;i<totnbins;i++) {
        npairs[i]=0;
    }
#ifdef OUTPUT_RPAVG
    DOUBLE rpavg[totnbins];
    for(int i=0;i<totnbins;i++) {
        rpavg[i]=0;
    }
#endif//OUTPUT_RPAVG

    const DOUBLE dpi = pimax/npibin;
    const DOUBLE inv_dpi = 1.0/dpi;
    for(int64_t i=0;i<N0;i++) {
        const DOUBLE xpos = *x0++;
        const DOUBLE ypos = *y0++;
        const DOUBLE zpos = *z0++;
        const DOUBLE dpos = *d0++;

        int64_t j = (same_cell == 1) ? (i+1):0;
        if(same_cell == 0) {
            DOUBLE *locald1 = d1;
            while(j < N1) {
                const DOUBLE dz = *locald1++ - dpos;
                if(dz > -pimax) break;
                j++;
            }
        }
        DOUBLE *localx1 = x1 + j;
        DOUBLE *localy1 = y1 + j;
        DOUBLE *localz1 = z1 + j;

        for(;j<N1;j++){
            const DOUBLE parx = xpos + *localx1;
            const DOUBLE pary = ypos + *localy1;
            const DOUBLE parz = zpos + *localz1;
            
            const DOUBLE perpx = xpos - *localx1;
            const DOUBLE perpy = ypos - *localy1;
            const DOUBLE perpz = zpos - *localz1;

            localx1++;localy1++;localz1++;
            
            const DOUBLE sqr_s = perpx*perpx + perpy*perpy + perpz*perpz;
            if(sqr_s >= sqr_max_sep) continue;
            
            const DOUBLE tmp  = (parx*perpx+pary*perpy+parz*perpz);
            const DOUBLE tmp1 = (parx*parx+pary*pary+parz*parz);
            const DOUBLE sqr_Dpar = (tmp*tmp)/tmp1;
            if(sqr_Dpar >= sqr_pimax) continue;
            
            const int pibin  = (sqr_Dpar >= sqr_pimax) ? npibin:(int) (SQRT(sqr_Dpar)*inv_dpi);
            const DOUBLE sqr_Dperp  = sqr_s - sqr_Dpar;
            if(sqr_Dperp >= sqr_rpmax || sqr_Dperp < sqr_rpmin) continue;
#ifdef OUTPUT_RPAVG
            const DOUBLE rp = SQRT(sqr_Dperp);
#endif
            
            for(int kbin=nbin-1;kbin>=1;kbin--) {
                if(sqr_Dperp >= rupp_sqr[kbin-1]) {
                    const int ibin = kbin*(npibin+1) + pibin;
                    npairs[ibin]++;
#ifdef OUTPUT_RPAVG
                    rpavg[ibin]+=rp;
#endif
                    break;
                }
            }//finding kbin
        }//j loop over second set of particles
    }//i loop over first set of particles

    for(int i=0;i<totnbins;i++) {
        src_npairs[i] += npairs[i];
#ifdef OUTPUT_RPAVG
        src_rpavg[i] += rpavg[i];
#endif        
    }
}//end of naive code


    
