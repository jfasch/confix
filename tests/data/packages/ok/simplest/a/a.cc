#include "a.h"

// CONFIX:REQUIRE_H('b.h')

extern "C" int b();

namespace a {

int a() {
    return b();
}

}; // /namespace
