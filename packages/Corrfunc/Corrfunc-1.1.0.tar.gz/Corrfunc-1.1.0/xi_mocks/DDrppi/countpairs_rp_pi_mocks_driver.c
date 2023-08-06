/* File: countpairs_rp_pi_mocks_driver.c */
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

#include "defs.h"//minimal header macros that might be useful generally
#include "countpairs_rp_pi_mocks_driver.h"//the function prototypes + function_precision.h

//directly include the kernel file with
//actual implementations. The appropriate
//AVX or SSE header files are included in the
//kernel files
#include "countpairs_rp_pi_mocks_kernels.c"

void countpairs_rp_pi_mocks_driver(DOUBLE *x0, DOUBLE *y0, DOUBLE *z0, DOUBLE *d0, const int64_t N0,
                                   DOUBLE *x1, DOUBLE *y1, DOUBLE *z1, DOUBLE *d1, const int64_t N1,
                                   const int same_cell
#ifdef PERIODIC
                                   ,const DOUBLE off_xwrap, const DOUBLE off_ywrap, const DOUBLE off_zwrap
#endif                        
                                   ,const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const int npibin, const DOUBLE *rupp_sqr, const DOUBLE pimax
                                   
#ifdef OUTPUT_RPAVG
                                   ,DOUBLE *src_rpavg
#endif
                                   ,uint64_t *src_npairs)
{

    const int64_t totnbins = (npibin+1)*(nbin+1);
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

#if defined(USE_AVX) && defined(__AVX__)
    /*----------------- AVX --------------------*/
    AVX_FLOATS m_rupp_sqr[nbin];
    for(int i=0;i<nbin;i++) {
        m_rupp_sqr[i] = AVX_SET_FLOAT(rupp_sqr[i]);
    }
    AVX_FLOATS m_kbin[nbin];
    for(int i=0;i<nbin;i++) {
        m_kbin[i] = AVX_SET_FLOAT((DOUBLE) i);
    }
#warning using avx
    countpairs_rp_pi_mocks_avx_intrinsics(x0, y0, z0, d0, N0,
                                          x1, y1, z1, d1, N1, same_cell,
                                          sqr_rpmax, sqr_rpmin, nbin, npibin, rupp_sqr, pimax
                                          ,m_rupp_sqr
                                          ,m_kbin
#ifdef OUTPUT_RPAVG
                                          ,rpavg
#endif                         
                                          ,npairs);

#else //AVX
#if defined (__SSE4_2__)

    /*------------------ SSE -------------------*/
    SSE_FLOATS m_rupp_sqr[nbin];
    for(int i=0;i<nbin;i++) {
        m_rupp_sqr[i] = SSE_SET_FLOAT(rupp_sqr[i]);
    }
    SSE_FLOATS m_kbin[nbin];
    for(int i=0;i<nbin;i++) {
        m_kbin[i] = SSE_SET_FLOAT((DOUBLE) i);
    }
#warning using sse
    countpairs_rp_pi_mocks_sse_intrinsics(x0, y0, z0, d0, N0,
                                          x1, y1, z1, d1, N1, same_cell,
                                          sqr_rpmax, sqr_rpmin, nbin, npibin, rupp_sqr, pimax
                                          ,m_rupp_sqr
                                          ,m_kbin
#ifdef OUTPUT_RPAVG
                                          ,rpavg
#endif                         
                                          ,npairs);

#else //SSE

    /*----------------- FALLBACK CODE --------------------*/
    countpairs_rp_pi_mocks_naive(x0, y0, z0, d0, N0,
                                 x1, y1, z1, d1, N1, same_cell,
                                 sqr_rpmax, sqr_rpmin,  nbin, npibin, rupp_sqr, pimax
#ifdef OUTPUT_RPAVG
                                 ,rpavg
#endif                         
                                 ,npairs);


#endif//SSE
#endif//AVX

    for(int i=0;i<totnbins;i++) {
        src_npairs[i] += npairs[i];
#ifdef OUTPUT_RPAVG
        src_rpavg[i] += rpavg[i];
#endif        
    }
    return;
}    

#if 0
    const int64_t block_size = 32;
    for(int64_t i=0;i<N0;i+=block_size) {
        const DOUBLE dpos = d0[i];
        const int64_t block_size1 = (N0-i) > block_size ? block_size:(N0-i);

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
        
        for(;j<N1;j+=block_size) {
            const int64_t block_size2 = (N1-j) > block_size ? block_size:(N1-j);
#if defined(USE_AVX) && defined(__AVX__)            
            //AVX is available and wanted -> call the AVX function
#else //AVX
#if defined (__SSE4_2__)
#else//NOT SSE or AVX -> call naive code
            
            /*----------------- FALLBACK CODE --------------------*/
            countpairs_rp_pi_mocks_naive(&x0[i], &y0[i], &z0[i], block_size1,
                                         localx1, localy1, localz1, block_size2, 
                                         sqr_rpmax, sqr_rpmin,  nbin, npibin, rupp_sqr, pimax
#ifdef OUTPUT_RPAVG
                                         ,rpavg
#endif                         
                                         ,npairs);
            
#endif//SSE4.2
#endif//AVX            
            
        }
    }
}    
#endif
