#ifndef TEST_UTILS_HPP
#define TEST_UTILS_HPP
#pragma once

#include "catch.hpp"
#include <string>
#include <sstream>

//=============================================================================
//  This file adds convenient REQUIRE_* macros so you can test your
//  solution more conveniently.
//
//  You can write your own REQUIRE_* or CHECK_* macros here if you
//  are brave enough.
//=============================================================================

/**
 * Tries to instantiate the constructor and expects that
 *
 *      Complain::invalidWorld(line, ...)
 *
 * gets called.
 *
 * \param   WORLD       world stringstream
 * \param   SOURCE      source stringstream
 * \param   LINE        line on which the error is expected to be reported
 */
#define REQUIRE_INVALID_WORLD(WORLD, SOURCE, LINE)                  \
    do {                                                            \
        decltype(LINE)    _l   = (LINE);                            \
        std::stringstream _msg;                                     \
        _msg << "invalid world: on line " << _l;                    \
        REQUIRE_THROWS_WITH(                                        \
            [&](){ Interpret _(WORLD, SOURCE); }(),                 \
            Catch::StartsWith(_msg.str())                           \
        );                                                          \
    } while (0)

/**
 * Tries to instantiate the constructor and expects that
 *
 *      Complain::invalidSource(line, ...)
 *
 * gets called.
 *
 * \param   WORLD       world stringstream
 * \param   SOURCE      source stringstream
 * \param   LINE        line on which the error is expected to be reported
 */
#define REQUIRE_INVALID_SOURCE(WORLD, SOURCE, LINE)                 \
    do {                                                            \
        decltype(LINE)    _l   = (LINE);                            \
        std::stringstream _msg;                                     \
        _msg << "invalid source: on line " << _l;                   \
        REQUIRE_THROWS_WITH(                                        \
            [&](){ Interpret _(WORLD, SOURCE); }(),                 \
            Catch::StartsWith(_msg.str())                           \
        );                                                          \
    } while (0)

/**
 * Tries to instantiate the constructor and expects that
 *
 *      Complain::undefinedReference(from, to, ...)
 *
 * gets called.
 *
 * \param   WORLD       world stringstream
 * \param   SOURCE      source stringstream
 * \param   FROM        name of the procedure that contains invalid call
 * \param   TO          target of the invalid call
 */
#define REQUIRE_UNDEFINED_REFERENCE(WORLD, SOURCE, FROM, TO)        \
    do {                                                            \
        std::string&& _f = (FROM);                                  \
        std::string&& _t = (TO);                                    \
        std::stringstream _msg;                                     \
        _msg << "undefined reference: " << _f << " calls " << _t;   \
        REQUIRE_THROWS_WITH(                                        \
            [&](){ Interpret _(WORLD, SOURCE); }(),                 \
            Catch::StartsWith(_msg.str())                           \
        );                                                          \
    } while (0)

/**
 * Executes the given expression of the interpret and expects that
 *
 *      Complain::runtimeError(procedure, index, ...)
 *
 * gets called. Use with run or step like this:
 *
 *      Interpret interpret(...);   // constructor
 *      // option A (run)
 *      REQUIRE_RUNTIME_ERROR(interpret.run(), "MAIN", 0u);
 *      // option B (step)
 *      REQUIRE_RUNTIME_ERROR(interpret.step(), "MAIN", 0u);
 *
 * \param   EXPR        expression to be executed
 * \param   PROCEDURE   name of the procedure that should cause an error
 * \param   INDEX       index of the instruction that should cause an error
 */
#define REQUIRE_RUNTIME_ERROR(EXPR, PROCEDURE, INDEX)               \
    do {                                                            \
        std::string&&     _p = (PROCEDURE);                         \
        decltype(INDEX)   _i = (INDEX);                             \
        std::stringstream _msg;                                     \
        _msg << "runtime error: in " << _p                          \
             << " on instruction " << _i;                           \
        REQUIRE_THROWS_WITH(                                        \
            EXPR,                                                   \
            Catch::StartsWith(_msg.str())                           \
        );                                                          \
    } while (0)

#endif // TEST_UTILS_HPP
