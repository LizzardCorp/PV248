#ifndef INTERFACE_HPP
#define INTERFACE_HPP
#pragma once

#include <istream>
#include <string>

#include "defs.hpp"

//=============================================================================
//
//  This file describes interface required by the assignment.
//
//  You are NOT required to include this in your final solution.
//  Feel free to move these classes to different files and remove this one
//  if you feel like doing so.
//
//=============================================================================

//--  Robot  ------------------------------------------------------------------

/**
 * The Robot class represents the robot moving around in the world.
 */
class Robot
{
public:
    /**
     * Returns the current position of the robot.
     */
    Position position() const;

    /**
     * Returns the current direction of the robot.
     */
    Direction direction() const;
};

//--  World  ------------------------------------------------------------------

/**
 * The World class represents the world where the robot moves.
 */
class World
{
public:
    /**
     * Returns the width of the world, in tiles.
     */
    size_t width() const;

    /**
     * Returns the height of the world, in tiles.
     */
    size_t height() const;

    /**
     * Returns the tile on position tile.
     *
     * \param   where       the position of the desired tile.
     * \note    The return value is undefined if the \p where
     *          parameter is not a valid position in the world.
     */
    Tile tile(Position where) const;
};

//--  Interpret  --------------------------------------------------------------

/**
 * The Interpret class defines operations on the interpret.
 */
class Interpret
{
public:
    /**
     * Parses input files and initializes the interpret.
     *
     * \param   world       stream with the world definition
     * \param   program     stream with the program source definition
     *
     * \note    Calls Complain::invalidSource, Complain::invalidWorld
     *          or Complain::undefinedReference on errors in the source.
     * \note    After successful initialization the interpret shall
     *          be in the \a running state with the \c MAIN as the
     *          active procedure.
     */
    Interpret(std::istream& world, std::istream& program);

    /**
     * Returns a constant reference to the Robot.
     * The robot changes as the program is being interpreted.
     */
    const Robot& robot() const;

    /**
     * Returns a constant reference to the World.
     * The world changes as the program is being interpreted.
     */
    const World& world() const;

    /**
     * Returns \c true if there exists a procedure named \p name.
     *
     * \param   name        name of the procedure to search for
     */
    bool hasProcedure(const std::string& name) const;

    /**
     * Returns \c true if the interpret is in the \a running state.
     */
    bool running() const;

    /**
     * Takes a single step in the program execution.
     * Does nothing if the interpret is in the \a stopped state.
     *
     * \returns \c true if the interpret remains in the \a running state.
     */
    bool step();

    /**
     * Executes all steps of the program until it ends.
     * Does nothing if the interpret is in the \a stopped state.
     *
     * \returns the number of steps the interpret took to finish the program
     */
    unsigned run();
};

#endif // INTERFACE_HPP
