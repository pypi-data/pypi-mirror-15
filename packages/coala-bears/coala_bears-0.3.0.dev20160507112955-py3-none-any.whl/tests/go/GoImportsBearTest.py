
from bears.go.GoImportsBear import GoImportsBear
from tests.LocalBearTestHelper import verify_local_bear

GoImportsBearTest = verify_local_bear(
    GoImportsBear,
    (['package main', '', 'import "os"', '',
      'func main() {', '\tf, _ := os.Open("foo")', '}'],),
    (['package main', '', '',
      'func main() {', '\tf, _ := os.Open("foo")', '}'],))
