#include <sstream>

#include "catch.hpp"
#include "test-utils.hpp"

// ADD HEADER FILES OF YOUR SOLUTION HERE
// #include "interface.hpp"

//=============================================================================
// This file shows example tests that may be an inspiration for your own.
// You are strongly advised to expand these tests as they only cover
// a hilariously small portion of the assignment.
//
// You can also create more test-.* files, but remember to call cmake
// each time you create a new file.
//=============================================================================

//--  Worlds  -----------------------------------------------------------------

// You will learn about namespaces later in the course.
namespace worlds
{
// For now let's just say that all symbols declared here
// should be called 'worlds::<name>' in your tests to avoid confusion
// with other data sets.

// trivial world from the assignment
static const std::string trivial =
    "1 1\n"
    "0 0 n\n"
    " \n";

// example of an invalid world from the assignment
static const std::string invalid =
    "4\t3\n"
    "1\t1\te\n"
    "####\n"
    "# 3#\n"
    "####\n"
    "####\n";

// Add additional world definitions here and use them in your own tests.
// Do NOT forget to add '\n' at the end of each line!

/*
static const std::string NAME =
    "...\n"
    "...\n";
*/

} // namespace worlds

//--  Sources  ----------------------------------------------------------------

namespace sources
{

// trivial source from the assignment
static const std::string trivial =
    "DEFINE MAIN\n"
    "END\n";

// example of an invalid source from the assignment
static const std::string invalid =
    "DEFINE else\n"
    "# This is a comment\n"
    "# Special characters like @#$%^ are allowed here\n"
    "# And so are empty lines\n"
    "\n"
    "   SKIP\n"
    "   IFWALL BREAK\n"
    "   SKIP\n"
    "   ELSE else\n"
    "END\n"
    "\n"
    "DEFINE MAIN\n"
    "# Indentation is not required\n"
    "else\n"
    "\t \t \t# Insane indentation is allowed\n"
    "           \t\t\t          END\n";

// example of undefined reference
static const std::string no_main =
    "DEFINE main\n"
    "END\n";

// example of program that should throw an error with the trivial world
// when executed
static const std::string pickup =
    "DEFINE MAIN\n"
    "PICKUP\n"
    "END\n";

// Add additional source codes here and use them in your own tests.
// Do NOT forget to add '\n' at the end of each line!

/*
static const std::string NAME =
    "...\n"
    "...\n";
*/

} // namespace sources

//-  Tests  -------------------------------------------------------------------

/*
 * In test-utils.hpp there are four REQUIRE_* macros declared
 * for your convenience.
 *
 * - to test Complain::invalidWorld call:
 *
 *      REQUIRE_INVALID_WORLD(world, source, line);
 *
 * - to test Complain::invalidSource call:
 *
 *      REQUIRE_INVALID_SOURCE(world, source, line);
 *
 * - to test Complain::undefinedReference call:
 *
 *      REQUIRE_UNDEFINED_REFERENCE(world, source, from, to);
 *
 * - to test Complain::runtimeError call:
 *
 *      REQUIRE_RUNTIME_ERROR(<expression>, procedure, index);
 *
 *   where <expression> can be one of
 *
 *      <Interpret instance>.run()
 *      <Interpret instance>.step()
 *
 * See the examples below or the documentation of test-utils.hpp.
 */

TEST_CASE("Trivial world and program (example)")
{
    std::stringstream world(worlds::trivial);
    std::stringstream source(sources::trivial);

    SECTION("constructor does not report any errors") {
        Interpret interpret(world, source);

        SECTION("interpret is running when created") {
            REQUIRE(interpret.running());
        }
    }
}

TEST_CASE("Invalid world (example)")
{
    std::stringstream world(worlds::invalid);
    std::stringstream source(sources::trivial);

    SECTION("constructor reports 'invalid world' on line 6") {
        REQUIRE_INVALID_WORLD(world, source, 6u);
    }
}

TEST_CASE("Invalid source (example)")
{
    std::stringstream world(worlds::trivial);
    std::stringstream source(sources::invalid);

    SECTION("constructor reports 'invalid source' on line 9") {
        REQUIRE_INVALID_SOURCE(world, source, 9u);
    }
}

TEST_CASE("Undefined reference (example)")
{
    std::stringstream world(worlds::trivial);
    std::stringstream source(sources::no_main);

    SECTION("constructor reports 'undefined reference' for @ENTRY") {
        REQUIRE_UNDEFINED_REFERENCE(world, source, "@ENTRY", "MAIN");
    }
}

TEST_CASE("Runtime error (example)")
{
    std::stringstream world(worlds::trivial);
    std::stringstream source(sources::pickup);

    SECTION("constructor does not report any errors") {
        Interpret interpret(world, source);

        SECTION("interpret reports 'runtime error' on PICKUP instruction") {
            REQUIRE_RUNTIME_ERROR(interpret.run(), "MAIN", 0u);
        }
    }
}
