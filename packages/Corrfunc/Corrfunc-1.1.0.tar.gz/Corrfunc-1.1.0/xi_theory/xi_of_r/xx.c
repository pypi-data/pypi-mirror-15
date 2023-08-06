            cellarray_index *first = &(lattice1[index1]);
            const int iz = index1 % nmesh_z ;
            const int ix = index1 / (nmesh_z * nmesh_y) ;
            const int iy = (index1 - iz - ix*nmesh_z*nmesh_y)/nmesh_z ;
            assert( ((iz + nmesh_z*iy + nmesh_z*nmesh_y*ix) == index1) && "Index reconstruction is wrong");
            for(int iix=-bin_refine_factor;iix<=bin_refine_factor;iix++){
                int iiix;
#ifdef PERIODIC
                DOUBLE off_xwrap=0.0;
                if(ix + iix >= nmesh_x) {
                    off_xwrap = -xdiff;
                } else if (ix + iix < 0) {
                    off_xwrap = xdiff;
                }
                iiix=(ix+iix+nmesh_x)%nmesh_x;
#else
                iiix = iix+ix;
                if(iiix < 0 || iiix >= nmesh_x) {
                    continue;
                }
#endif

                for(int iiy=-bin_refine_factor;iiy<=bin_refine_factor;iiy++){
                    int iiiy;
#ifdef PERIODIC
                    DOUBLE off_ywrap = 0.0;
                    if(iy + iiy >= nmesh_y) {
                        off_ywrap = -ydiff;
                    } else if (iy + iiy < 0) {
                        off_ywrap = ydiff;
                    }
                    iiiy=(iy+iiy+nmesh_y)%nmesh_y;
#else
                    iiiy = iiy+iy;
                    if(iiiy < 0 || iiiy >= nmesh_y) {
                        continue;
                    }
#endif

                    for(int iiz=-bin_refine_factor;iiz<=bin_refine_factor;iiz++){
                        int iiiz;
#ifdef PERIODIC
                        DOUBLE off_zwrap = 0.0;
                        if(iz + iiz >= nmesh_z) {
                            off_zwrap = -zdiff;
                        } else if (iz + iiz < 0) {
                            off_zwrap = zdiff;
                        }
                        iiiz=(iz+iiz+nmesh_z)%nmesh_z;
#else
                        iiiz = iiz+iz;
                        if(iiiz < 0 || iiiz >= nmesh_z) {
                            continue;
                        }
#endif
                        assert(iiix >= 0 && iiix < nmesh_x && iiiy >= 0 && iiiy < nmesh_y && iiiz >= 0 && iiiz < nmesh_z && "Checking that the second pointer is in range");
                        const int64_t index2 = iiix*nmesh_y*nmesh_z + iiiy*nmesh_z + iiiz;
                        const cellarray_index *second = &(lattice2[index2]);
                        DOUBLE *x1 = first->pos;
                        DOUBLE *y1 = (first->pos) + NVEC;
                        DOUBLE *z1 = (first->pos) + 2*NVEC;

                        DOUBLE *x2 = second->pos;
                        DOUBLE *y2 = (second->pos) + NVEC;
                        DOUBLE *z2 = (second->pos) + 2*NVEC;

                        for(int64_t i=0;i<first->nelements;i+=NVEC) {
                            int block_size1 = first->nelements - i;
                            if(block_size1 > NVEC) block_size1 = NVEC;

                            for(int ii=0;ii<block_size1;ii++) {
                                DOUBLE x1pos = x1[ii];
                                DOUBLE y1pos = y1[ii];
                                DOUBLE z1pos = z1[ii];

#ifdef PERIODIC
                                x1pos += off_xwrap;
                                y1pos += off_ywrap;
                                z1pos += off_zwrap;
#endif


#if !(defined(USE_AVX) && defined(__AVX__))

                                DOUBLE *localx2 = x2;
                                DOUBLE *localy2 = y2;
                                DOUBLE *localz2 = z2;

                                for(int64_t j=0;j<second->nelements;j+=NVEC) {
                                    int block_size2=second->nelements - j;
                                    if(block_size2 > NVEC) block_size2=NVEC;

                                    for(int jj=0;jj<block_size2;jj++) {
                                        const DOUBLE dx = x1pos - localx2[jj];
                                        const DOUBLE dy = y1pos - localy2[jj];
                                        const DOUBLE dz = z1pos - localz2[jj];
                                        const DOUBLE r2 = (dx*dx + dy*dy + dz*dz);
                                        if(r2 >= sqr_rpmax || r2 < sqr_rpmin) {
                                            continue;
                                        }
#ifdef OUTPUT_RPAVG
                                        const DOUBLE r = SQRT(r2);
#endif
                                        for(int kbin=nrpbin-1;kbin>=1;kbin--){
                                            if(r2 >= rupp_sqr[kbin-1]) {
                                                npairs[kbin]++;
#ifdef OUTPUT_RPAVG
                                                rpavg[kbin] += r;
#endif
                                                break;
                                            }
                                        }//searching for kbin loop
                                    }//end of jj loop

                                    localx2 += 3*NVEC;//this might actually exceed the allocated range but we will never dereference that
                                    localy2 += 3*NVEC;
                                    localz2 += 3*NVEC;

                                }//end of j loop

#else //beginning of AVX section

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

                                const AVX_FLOATS m_x1pos = AVX_SET_FLOAT(x1pos);
                                const AVX_FLOATS m_y1pos = AVX_SET_FLOAT(y1pos);
                                const AVX_FLOATS m_z1pos = AVX_SET_FLOAT(z1pos);

                                DOUBLE *localx2 = x2;
                                DOUBLE *localy2 = y2;
                                DOUBLE *localz2 = z2;

                                int64_t j;
                                for(j=0;j<=(second->nelements-NVEC);j+=NVEC) {
                                    //Load the x/y/z arrays (NVEC at a time)
                                    const AVX_FLOATS x2pos = AVX_LOAD_FLOATS_UNALIGNED(localx2);
                                    const AVX_FLOATS y2pos = AVX_LOAD_FLOATS_UNALIGNED(localy2);
                                    const AVX_FLOATS z2pos = AVX_LOAD_FLOATS_UNALIGNED(localz2);

                                    localx2 += 3*NVEC;//this might actually exceed the allocated range but we will never dereference that
                                    localy2 += 3*NVEC;
                                    localz2 += 3*NVEC;


                                    //x1-x2
                                    const AVX_FLOATS m_xdiff = AVX_SUBTRACT_FLOATS(m_x1pos,x2pos);
                                    //y1-y2
                                    const AVX_FLOATS m_ydiff = AVX_SUBTRACT_FLOATS(m_y1pos,y2pos);
                                    //z1-z2
                                    const AVX_FLOATS m_zdiff = AVX_SUBTRACT_FLOATS(m_z1pos,z2pos);

                                    //set constant := sqr_rpmax
                                    const AVX_FLOATS m_sqr_rpmax = AVX_SET_FLOAT(sqr_rpmax);
                                    //set constant := sqr_rpmin
                                    const AVX_FLOATS m_sqr_rpmin = AVX_SET_FLOAT(sqr_rpmin);

                                    //(x1-x2)^2
                                    const AVX_FLOATS m_xdiff_sqr = AVX_SQUARE_FLOAT(m_xdiff);

                                    //(y1-y2)^2
                                    const AVX_FLOATS m_ydiff_sqr = AVX_SQUARE_FLOAT(m_ydiff);

                                    //(z1-z2)^2
                                    const AVX_FLOATS m_zdiff_sqr = AVX_SQUARE_FLOAT(m_zdiff);

                                    //(x1-x2)^2 + (y1-y2)^2
                                    const AVX_FLOATS m_xydiff_sqr_sum = AVX_ADD_FLOATS(m_xdiff_sqr,m_ydiff_sqr);

                                    //r2 now will contain (x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2
                                    AVX_FLOATS r2 = AVX_ADD_FLOATS(m_zdiff_sqr,m_xydiff_sqr_sum);
                                    AVX_FLOATS m_mask_left;

                                    {

                                        //Create a mask for the NVEC distances that fall within sqr_rpmin and sqr_rpmax (sqr_rpmin <= dist < sqr_rpmax)
                                        const AVX_FLOATS m_rpmax_mask = AVX_COMPARE_FLOATS(r2, m_sqr_rpmax, _CMP_LT_OS);
                                        const AVX_FLOATS m_rpmin_mask = AVX_COMPARE_FLOATS(r2, m_sqr_rpmin, _CMP_GE_OS);
                                        const AVX_FLOATS m_rp_mask = AVX_BITWISE_AND(m_rpmax_mask,m_rpmin_mask);

                                        //Check if any of the NVEC distances are less than sqr_rpmax
                                        m_mask_left = m_rp_mask;

                                        //If all points are >= sqr_rpmax, continue with the j-loop
                                        if(AVX_TEST_COMPARISON(m_mask_left) == 0) {
                                            continue;
                                        }
                                        //Update r2 such that all distances that do not satisfy sqr_rpmin <= r2 < sqr_rpmax, get set to sqr_rpmax
                                        r2 = AVX_BLEND_FLOATS_WITH_MASK(m_sqr_rpmax, r2, m_mask_left);
                                    }


#ifdef OUTPUT_RPAVG
                                    //first do the sqrt since r2 contains squared distances
                                    union_mDperp.m_Dperp = AVX_SQRT_FLOAT(r2);
                                    AVX_FLOATS m_rpbin = AVX_SET_FLOAT((DOUBLE) 0.0);
#endif

                                    /* AVX_FLOATS m_all_ones  = AVX_CAST_INT_TO_FLOAT(AVX_SET_INT(-1));//-1 is 0xFFFF... and the cast just reinterprets (i.e., the cast is a no-op) */

                                    //Loop over the histogram bins backwards. Most pairs will fall into the outer bins -> more efficient to loop backwards
                                    //Remember that rupp[kbin-1] contains upper limit of previous bin -> lower radial limit of kbin
                                    for(int kbin=nrpbin-1;kbin>=1;kbin--) {
                                        //Create a mask of pairwise separations that are greater than the lower radial limit of this bin (kbin)
                                        const AVX_FLOATS m1 = AVX_COMPARE_FLOATS(r2,m_rupp_sqr[kbin-1],_CMP_GE_OS);
                                        //Do a bitwise AND to get the mask for separations that fall into this bin
                                        const AVX_FLOATS m_bin_mask = AVX_BITWISE_AND(m1,m_mask_left);
                                        //Create the mask for the remainder. This comparison should be exclusive with the comparison used for the m1 variable.
                                        m_mask_left = AVX_COMPARE_FLOATS(r2,m_rupp_sqr[kbin-1],_CMP_LT_OS);
                                        /* m_mask_left = AVX_XOR_FLOATS(m1, m_all_ones);//XOR with 0xFFFF... gives the bins that are smaller than m_rupp_sqr[kbin] (and is faster than cmp_p(s/d) in theory) */

                                        //Check the mask
                                        const int test2  = AVX_TEST_COMPARISON(m_bin_mask);

                                        //Do a pop-count to add the number of bits. This is somewhat wasteful, since
                                        //only 4 bits are set in DOUBLE_PREC mode (8 bits in regular float) but we
                                        //are adding up all 32 bits in the integer. However, in my massive amount of
                                        //testing with all sorts of faster implementations of popcount and table lookups,
                                        //builtin hardware popcnt always outperformed everything else. Thanks to NSA
                                        //for requiring a hardware popcnt I suppose.
                                        npairs[kbin] += AVX_BIT_COUNT_INT(test2);

                                        //Add the kbin variable (as float) into the m_rpbin variable.
                                        //This would be so much better implemented in AVX2 with support for integers
#ifdef OUTPUT_RPAVG
                                        m_rpbin = AVX_BLEND_FLOATS_WITH_MASK(m_rpbin,m_kbin[kbin], m_bin_mask);
#endif
                                        //Check if there are any more valid points left. Break out of the kbin histogram loop if none are left
                                        const int test3 = AVX_TEST_COMPARISON(m_mask_left);
                                        if(test3 == 0)
                                            break;
                                    }

                                    //Since the m_rpbin is an AVX float, I have to truncate to an int to get the bin numbers.
                                    //Only required when OUTPUT_RPAVG is enabled (i.e., the next jj-loop with the pragma unroll is in effect)
#ifdef OUTPUT_RPAVG
                                    union_rpbin.m_ibin = AVX_TRUNCATE_FLOAT_TO_INT(m_rpbin);

                                    /*                              //All these ops can be avoided (and anything leading to these) if the CPU */
                                    /*                              //supports AVX 512 mask_add operation */

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
                                }//end of j-loop with AVX intrinsics

                                //Now take care of the remainder.
                                for(int ipos=0;j<second->nelements;j++,ipos++) {
                                    const DOUBLE dx = x1pos - localx2[ipos];
                                    const DOUBLE dy = y1pos - localy2[ipos];
                                    const DOUBLE dz = z1pos - localz2[ipos];

                                    const DOUBLE r2 = (dx*dx + dy*dy + dz*dz);
                                    if(r2 >= sqr_rpmax || r2 < sqr_rpmin) {
                                        continue;
                                    }
#ifdef OUTPUT_RPAVG
                                    const DOUBLE r = SQRT(r2);
#endif
                                    for(int kbin=nrpbin-1;kbin>=1;kbin--){
                                        if(r2 >= rupp_sqr[kbin-1]) {
                                            npairs[kbin]++;
#ifdef OUTPUT_RPAVG
                                            rpavg[kbin] += r;
#endif
                                            break;
                                        }
                                    }//searching for kbin loop
                                }//end of remainder j loop

#endif//end of AVX section

                            }//end of ii loop

                            x1 += 3*NVEC;
                            y1 += 3*NVEC;
                            z1 += 3*NVEC;
                        }//end of i loop
                    }//iiz loop over bin_refine_factor
                }//iiy loop over bin_refine_factor
            }//iix loop over bin_refine_factor

