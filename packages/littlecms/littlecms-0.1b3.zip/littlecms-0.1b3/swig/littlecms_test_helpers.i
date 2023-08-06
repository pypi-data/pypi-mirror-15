/* Helpers for assisting the tests */

/* When creating new profiles, there are two fields in the profile header which
 * vary when all other data is identical, the profile datetime and the platform.
 * This makes it harder to run tests because the Profile ID varies between runs
 * of the same test for these reasons.
 * The datetime can be set with the helper function here.
 * The platform cannot be set without modifying the LittleCMS library. So tests
 * will need two reference Profile IDs, one for Windows and one for other, because
 * those are the two options _cmsWriteHeader() has.
 */
%inline %{
  #include <time.h>
  #include "lcms2_internal.h"

  /* Set the profile datetime to a fixed value. */
  void set_datetime(cmsHPROFILE hProfile, cmsDateTimeNumber *datetime)
  {
    _cmsICCPROFILE *profile = (_cmsICCPROFILE *) hProfile;
	profile->Created.tm_year = datetime->year;
	profile->Created.tm_mon = datetime->month;
	profile->Created.tm_mday = datetime->day;
	profile->Created.tm_hour = datetime->hours;
	profile->Created.tm_min = datetime->minutes;
	profile->Created.tm_sec = datetime->seconds;
	profile->Created.tm_wday = 0;
	profile->Created.tm_yday = 0;
	profile->Created.tm_isdst = 0;
  }
%}
