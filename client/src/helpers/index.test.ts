import { translateCouponValuesToDates } from '.';
import {
  CourseJSONWithCouponsAndQuotes,
  CourseJSONWithoutCouponsAndQuotes,
} from '../tests/data';

describe('translateCouponValuesToDates', () => {
  test('does not change course without coupons', () => {
    const translatedCourse = translateCouponValuesToDates(CourseJSONWithoutCouponsAndQuotes);
    expect(translatedCourse).toEqual(CourseJSONWithoutCouponsAndQuotes);
  });
  test('translates dates for course with coupons', () => {
    const translatedCourse = translateCouponValuesToDates(CourseJSONWithCouponsAndQuotes);

    translatedCourse.coupons?.forEach((coupon) => {
      expect(coupon.utcExpiration).toEqual(new Date('2020-11-17T20:01:03.182265+00:00'));
    });
  });
});