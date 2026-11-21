/* Signed 32-bit scaling with a full 64-bit product and nearest rounding. */
/* Preserve Windows' observed signed-magnitude overflow boundary, including
 * nonzero INT_MIN products; zero products remain valid. */
static int MS f_MulDiv(int number,int numerator,int denominator){
 if(!denominator)return -1;if((number==INT32_MIN&&numerator)||(numerator==INT32_MIN&&number))return -1;int64_t product=(int64_t)number*numerator;unsigned negative=(product<0)^(denominator<0);
 uint64_t magnitude=(uint64_t)(product<0?-product:product),divisor=(uint64_t)(denominator<0?-(int64_t)denominator:denominator);
 uint64_t rounded=(magnitude+divisor/2)/divisor;if(rounded>INT32_MAX)return -1;return negative?-(int)rounded:(int)rounded;
}
