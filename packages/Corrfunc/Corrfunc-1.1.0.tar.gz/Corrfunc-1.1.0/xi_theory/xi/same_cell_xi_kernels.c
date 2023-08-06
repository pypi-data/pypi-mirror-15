/* File: same_cell_xi_kernels.c */
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


static inline void same_cell_xi_avx_intrinsics(DOUBLE *x1, DOUBLE *y1, DOUBLE *z1, const int64_t N1,
                                               const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const DOUBLE rupp_sqr[] , const DOUBLE pimax
                                               ,const AVX_FLOATS m_rupp_sqr[] 
#ifdef OUTPUT_RPAVG
                                               ,const AVX_FLOATS m_kbin[]
#endif                                            
                                               
#ifdef OUTPUT_RPAVG
                                               ,DOUBLE src_rpavg[]
#endif                         
                                               ,uint64_t *src_npairs)
{
    uint64_t npair[nbin];
    for(int i=0;i<nbin;i++) {
        npair[i] = 0;
    }
#ifdef OUTPUT_RPAVG
    DOUBLE rpavg[nbin];
    for(int i=0;i<nbin;i++) {
        rpavg[i] = 0.0;
    }
#endif    

    for(int64_t i=0;i<N1;i++) {
        const DOUBLE x1pos = *x1++;
        const DOUBLE y1pos = *y1++;
        const DOUBLE z1pos = *z1++;
        
        DOUBLE *x2 = x1;
        DOUBLE *y2 = y1;
        DOUBLE *z2 = z1;

        int64_t j=i+1;
        for(;j<=(N1-NVEC);j+=NVEC) {
#if !(defined(USE_AVX) && defined(__AVX__))
            for(int jj=0;jj<NVEC;jj++) {
                const DOUBLE dx = *x2++ - x1pos;
                const DOUBLE dy = *y2++ - y1pos;
                const DOUBLE dz = *z2++ - z1pos;
                
                if(dz >= pimax) {
                    j = N1;
                    break;
                }

                
                const DOUBLE r2 = dx*dx + dy*dy  + dz*dz;
                if(r2 >= sqr_rpmax || r2 < sqr_rpmin) {
                    continue;
                }
                
#ifdef OUTPUT_RPAVG
                const DOUBLE r = SQRT(r2);
#endif
                for(int kbin=nbin-1;kbin>=1;kbin--) {
                    if(r2 >= rupp_sqr[kbin-1]) {
                        npair[kbin]++;
#ifdef OUTPUT_RPAVG
                        rpavg[kbin]+=r;
#endif
                        break;
                    }
                }
            }//end of jj loop
#else
            const AVX_FLOATS m_xpos    = AVX_SET_FLOAT(x1pos);
            const AVX_FLOATS m_ypos    = AVX_SET_FLOAT(y1pos);
            const AVX_FLOATS m_zpos    = AVX_SET_FLOAT(z1pos);
            
#ifdef OUTPUT_RPAVG
            union int8 {
                AVX_INTS m_ibin;
                int ibin[NVEC];
            };
            union int8 union_rpbin;
            
            union float8{
                AVX_FLOATS m_Dperp;
                DOUBLE Dperp[NVEC];
            };
            union float8 union_mDperp;
#endif
            const AVX_FLOATS m_x2 = AVX_LOAD_FLOATS_UNALIGNED(x2);
            const AVX_FLOATS m_y2 = AVX_LOAD_FLOATS_UNALIGNED(y2);
            const AVX_FLOATS m_z2 = AVX_LOAD_FLOATS_UNALIGNED(z2);
            
            x2 += NVEC;//this might actually exceed the allocated range but we will never dereference that
            y2 += NVEC;
            z2 += NVEC;
            
            const AVX_FLOATS m_pimax = AVX_SET_FLOAT(pimax);
            const AVX_FLOATS m_zero  = AVX_SET_FLOAT(ZERO);
            
            const AVX_FLOATS m_zdiff = AVX_SUBTRACT_FLOATS(m_z2,m_zpos);//z2[j:j+NVEC-1] - z1
            const AVX_FLOATS m_sqr_xdiff = AVX_SQUARE_FLOAT(AVX_SUBTRACT_FLOATS(m_xpos,m_x2));//(x0 - x[j])^2
            const AVX_FLOATS m_sqr_ydiff = AVX_SQUARE_FLOAT(AVX_SUBTRACT_FLOATS(m_ypos,m_y2));//(y0 - y[j])^2
            const AVX_FLOATS m_sqr_zdiff = AVX_SQUARE_FLOAT(m_zdiff);
            AVX_FLOATS r2  = AVX_ADD_FLOATS(m_sqr_xdiff,AVX_ADD_FLOATS(m_sqr_ydiff, m_sqr_zdiff));
            
            AVX_FLOATS m_mask_left;
            
            //Do all the distance cuts using masks here in new scope
            {
                //the z2 arrays are sorted in increasing order. which means
                //the z2 value will increase in any future iteration of j.
                //that implies the zdiff values are also monotonically increasing
                //Therefore, if none of the zdiff values are less than pimax, then
                //no future iteration in j can produce a zdiff value less than pimax.
                //The code terminates the j-loop early in that case (and also sets
                //j equal to N1 to ensure that the remainder loop
                //does not run either.
                AVX_FLOATS m_mask_pimax = AVX_COMPARE_FLOATS(m_zdiff,m_pimax,_CMP_LT_OS);
                if(AVX_TEST_COMPARISON(m_mask_pimax) == 0) {
                    //If the execution reaches here -> then none of the NVEC zdiff values
                    //are smaller than pimax. We can terminate the j-loop now.
                    
                    //set j so that the remainder loop does not run
                    j = N1;
                    //break out of the j-loop
                    break;
                }
                
                /* //Create a mask with true bits when  0 <= zdiff < pimax. */
                m_mask_pimax = AVX_BITWISE_AND(AVX_COMPARE_FLOATS(m_zdiff,m_zero,_CMP_GE_OS),m_mask_pimax);
                const AVX_FLOATS m_rpmax_mask = AVX_COMPARE_FLOATS(r2, m_rupp_sqr[nbin-1], _CMP_LT_OS);
                const AVX_FLOATS m_rpmin_mask = AVX_COMPARE_FLOATS(r2, m_rupp_sqr[0], _CMP_GE_OS);
                const AVX_FLOATS m_rp_mask = AVX_BITWISE_AND(m_rpmax_mask,m_rpmin_mask);
                
                //Create a combined mask by bitwise and of m1 and m_mask_left.
                //This gives us the mask for all sqr_rpmin <= r2 < sqr_rpmax
                m_mask_left = AVX_BITWISE_AND(m_mask_pimax,m_rp_mask);

                
                //If not, continue with the next iteration of j-loop
                if(AVX_TEST_COMPARISON(m_mask_left) == 0) {
                    continue;
                }
                
                //There is some r2 that satisfies sqr_rpmin <= r2 < sqr_rpmax && dz < pimax.
                r2 = AVX_BLEND_FLOATS_WITH_MASK(m_rupp_sqr[nbin-1], r2, m_mask_left);
            }
            
#ifdef OUTPUT_RPAVG
            union_mDperp.m_Dperp = AVX_SQRT_FLOAT(r2);
            AVX_FLOATS m_rpbin = AVX_SET_FLOAT((DOUBLE) 0.0);
#endif
            
            //Loop backwards through nbins. m_mask_left contains all the points that are less than rpmax
            for(int kbin=nbin-1;kbin>=1;kbin--) {
                const AVX_FLOATS m1 = AVX_COMPARE_FLOATS(r2,m_rupp_sqr[kbin-1],_CMP_GE_OS);
                const AVX_FLOATS m_bin_mask = AVX_BITWISE_AND(m1,m_mask_left);
                const int test2  = AVX_TEST_COMPARISON(m_bin_mask);
                npair[kbin] += AVX_BIT_COUNT_INT(test2);
#ifdef OUTPUT_RPAVG
                m_rpbin = AVX_BLEND_FLOATS_WITH_MASK(m_rpbin,m_kbin[kbin], m_bin_mask);
#endif
                m_mask_left = AVX_COMPARE_FLOATS(r2,m_rupp_sqr[kbin-1],_CMP_LT_OS);
                const int test3 = AVX_TEST_COMPARISON(m_mask_left);
                if(test3 == 0) {
                    break;
                }
            }
            
#ifdef OUTPUT_RPAVG
            union_rpbin.m_ibin = AVX_TRUNCATE_FLOAT_TO_INT(m_rpbin);
            //protect the unroll pragma in case compiler is not icc.
#if  __INTEL_COMPILER
#pragma unroll(NVEC)
#endif
            for(int jj=0;jj<NVEC;jj++) {
                const int kbin = union_rpbin.ibin[jj];
                const DOUBLE r = union_mDperp.Dperp[jj];
                rpavg[kbin] += r;
            }
#endif//OUTPUT_RPAVG
#endif//end of AVX section               
        }//end of j-loop

        //remainder loop 
        for(;j<N1;j++){
            const DOUBLE dz = *z2++ - z1pos;
            const DOUBLE dx = *x2++ - x1pos;
            const DOUBLE dy = *y2++ - y1pos;
            
            if(dz >= pimax ) {
                break;
            }
            
            const DOUBLE r2 = dx*dx + dy*dy + dz*dz ;
            if(r2 >= sqr_rpmax || r2 < sqr_rpmin) {
                continue;
            }
            
#ifdef OUTPUT_RPAVG
            const DOUBLE r = SQRT(r2);
#endif

            for(int kbin=nbin-1;kbin>=1;kbin--) {
                if(r2 >= rupp_sqr[kbin-1]) {
                    npair[kbin]++;
#ifdef OUTPUT_RPAVG
                    rpavg[kbin] += r;
#endif
                    break;
                }
            }
        }//remainder loop over cellstruct first
    }//outer loop over cellstruct first

    for(int i=0;i<nbin;i++) {
        src_npairs[i] += npair[i];
#ifdef OUTPUT_RPAVG
        src_rpavg[i]  += rpavg[i];
#endif        
    }
}    
#endif//AVX


#if defined (__SSE4_2__)
#include "sse_calls.h"

static inline void same_cell_xi_sse_intrinsics(DOUBLE * x0, DOUBLE * y0, DOUBLE * z0, const int64_t N0,
                                               const DOUBLE sqr_rpmax, const DOUBLE sqr_rpmin, const int nbin, const DOUBLE rupp_sqr[] , const DOUBLE pimax
                                               ,const SSE_FLOATS m_rupp_sqr[] 
#ifdef OUTPUT_RPAVG
                                               ,const SSE_FLOATS m_kbin[]
                                               ,DOUBLE src_rpavg[]
#endif                         
                                               ,uint64_t *src_npairs)
{
    uint64_t *npairs = my_calloc(sizeof(*npairs), nbin);
#ifdef OUTPUT_RPAVG
    DOUBLE rpavg[nbin];
    for(int i=0;i<nbin;i++) {
        rpavg[i] = ZERO;
    }
#endif    

    for(int64_t i=0;i<N0;i++) {
        const DOUBLE xpos = *x0++;
        const DOUBLE ypos = *y0++;
        const DOUBLE zpos = *z0++;
        
		DOUBLE *x1 = x0;
		DOUBLE *y1 = y0;
		DOUBLE *z1 = z0;

		int64_t j = i+1;		
		for(;j<=(N0 - SSE_NVEC);j+=SSE_NVEC){

#ifdef OUTPUT_RPAVG
            union int4{
                SSE_INTS m_ibin;
                int ibin[SSE_NVEC];
            };
            union int4 union_rpbin;
            
            union float4{
                SSE_FLOATS m_Dperp;
                DOUBLE Dperp[SSE_NVEC];
            };
            union float4 union_mDperp;
#endif
            const SSE_FLOATS m_xpos = SSE_SET_FLOAT(xpos);
            const SSE_FLOATS m_ypos = SSE_SET_FLOAT(ypos);
            const SSE_FLOATS m_zpos = SSE_SET_FLOAT(zpos);

            const SSE_FLOATS m_x1 = SSE_LOAD_FLOATS_UNALIGNED(x1);
			const SSE_FLOATS m_y1 = SSE_LOAD_FLOATS_UNALIGNED(y1);
			const SSE_FLOATS m_z1 = SSE_LOAD_FLOATS_UNALIGNED(z1);

			x1 += SSE_NVEC;
			y1 += SSE_NVEC;
			z1 += SSE_NVEC;

            const SSE_FLOATS m_pimax = SSE_SET_FLOAT(pimax);
            /* const SSE_FLOATS m_zero  = SSE_SET_FLOAT(ZERO); */
            
            //set constant := sqr_rpmax
			const SSE_FLOATS m_sqr_rpmax = SSE_SET_FLOAT(sqr_rpmax);
			//set constant := sqr_rpmin
			const SSE_FLOATS m_sqr_rpmin = SSE_SET_FLOAT(sqr_rpmin);
			

			const SSE_FLOATS m_sqr_xdiff = SSE_SQUARE_FLOAT(SSE_SUBTRACT_FLOATS(m_x1, m_xpos));
            const SSE_FLOATS m_sqr_ydiff = SSE_SQUARE_FLOAT(SSE_SUBTRACT_FLOATS(m_y1, m_ypos));
            const SSE_FLOATS m_zdiff = SSE_SUBTRACT_FLOATS(m_z1, m_zpos);
            const SSE_FLOATS m_sqr_zdiff = SSE_SQUARE_FLOAT(m_zdiff);
            
            SSE_FLOATS r2  = SSE_ADD_FLOATS(m_sqr_zdiff,SSE_ADD_FLOATS(m_sqr_xdiff,m_sqr_ydiff));
            SSE_FLOATS m_mask_left;
			{
                const SSE_FLOATS m_pimax_mask = SSE_COMPARE_FLOATS_LT(m_zdiff,m_pimax);
                if(SSE_TEST_COMPARISON(m_pimax_mask) == 0) {
                    j = N0;
                    break;
                }
                
                const SSE_FLOATS m_rpmin_mask = SSE_COMPARE_FLOATS_GE(r2, m_sqr_rpmin);
                const SSE_FLOATS m_rpmax_mask = SSE_COMPARE_FLOATS_LT(r2,m_sqr_rpmax);
                const SSE_FLOATS m_rp_mask = SSE_BITWISE_AND(m_rpmin_mask, m_rpmax_mask);
                m_mask_left = SSE_BITWISE_AND(m_pimax_mask, m_rp_mask);
				if(SSE_TEST_COMPARISON(m_mask_left) == 0) {
					continue;
				}
				r2 = SSE_BLEND_FLOATS_WITH_MASK(m_sqr_rpmax, r2, m_mask_left);
            }
                
#ifdef OUTPUT_RPAVG
            union_mDperp.m_Dperp = SSE_SQRT_FLOAT(r2);
            SSE_FLOATS m_rpbin = SSE_SET_FLOAT(ZERO);
#endif

			for(int kbin=nbin-1;kbin>=1;kbin--) {
				SSE_FLOATS m1 = SSE_COMPARE_FLOATS_GE(r2,m_rupp_sqr[kbin-1]);
				SSE_FLOATS m_bin_mask = SSE_BITWISE_AND(m1,m_mask_left);
				m_mask_left = SSE_COMPARE_FLOATS_LT(r2,m_rupp_sqr[kbin-1]);
				int test2  = SSE_TEST_COMPARISON(m_bin_mask);
				npairs[kbin] += SSE_BIT_COUNT_INT(test2);
#ifdef OUTPUT_RPAVG
                m_rpbin = SSE_BLEND_FLOATS_WITH_MASK(m_rpbin,m_kbin[kbin], m_bin_mask);
#endif
				int test3 = SSE_TEST_COMPARISON(m_mask_left);
				if(test3 == 0) {
					break;
				}
			}

#ifdef OUTPUT_RPAVG
            union_rpbin.m_ibin = SSE_TRUNCATE_FLOAT_TO_INT(m_rpbin);
            //protect the unroll pragma in case compiler is not icc.
#if  __INTEL_COMPILER
#pragma unroll(SSE_NVEC)
#endif
            for(int jj=0;jj<SSE_NVEC;jj++) {
                const int kbin = union_rpbin.ibin[jj];
                const DOUBLE r = union_mDperp.Dperp[jj];
                rpavg[kbin] += r;
            }
#endif//OUTPUT_RPAVG
            
		}			

		for(;j<N0;j++) {
			const DOUBLE dx = *x1++ - xpos;
			const DOUBLE dy = *y1++ - ypos;
			const DOUBLE dz = *z1++ - zpos;
            if(dz >= pimax) break;
            
			const DOUBLE r2 = dx*dx + dy*dy + dz*dz;
			if(r2 >= sqr_rpmax || r2 < sqr_rpmin) continue;
#ifdef OUTPUT_RPAVG
            const DOUBLE r = SQRT(r2);
#endif            
			for(int kbin=nbin-1;kbin>=1;kbin--){
				if(r2 >= rupp_sqr[kbin-1]) {
					npairs[kbin]++;
#ifdef OUTPUT_RPAVG
                    rpavg[kbin] += r;
#endif                    
					break;
				}
			}//searching for kbin loop
		}
    }

	for(int i=0;i<nbin;i++) {
		src_npairs[i] += npairs[i];
#ifdef OUTPUT_RPAVG
        src_rpavg[i] += rpavg[i];
#endif        
        
	}
	free(npairs);
}

#endif //SSE 4.2

