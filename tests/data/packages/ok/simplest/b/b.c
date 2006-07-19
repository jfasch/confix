#include "b.h"

// CONFIX:REQUIRE_SYMBOL('c')

extern int c(void);

int b(void) {
    return c();
}
