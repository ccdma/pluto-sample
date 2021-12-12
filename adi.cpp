#include <stdio.h>
#include "iio.h"

int main(){
	
	struct iio_scan_context *info;
	info = iio_create_scan_context(NULL, 0);
	const char* uri = iio_context_info_get_uri(info);
	printf("%s\n", uri);
	return 0;
}