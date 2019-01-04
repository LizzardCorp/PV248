#include <cerrno>
#include <cstring>
#include <iostream>
#include <fstream>

// ADD HEADER FILES OF YOUR SOLUTION HERE
// #include "interface.hpp"

/**
 * This is an extremely simple demo program for the interpret.
 * It opens two files given as program parameters, feeds them to the
 * constructor of the interpret and then runs the program.
 *
 * If the program finishes successfully, it prints out the world.
 * Robot position is shown as 'n', 's', 'w' or 'e' as his
 * direction, or an uppercase letter if it stands on at least one mark.
 *
 * Usage:
 *      ./robot-cli WORLD PROGRAM
 *
 *  WORLD       path to the world definition
 *  PROGRAM     path to the program source
 */
int main(int argc, char *argv[])
{
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " WORLD PROGRAM" << std::endl;
        return EXIT_FAILURE;
    }

    // try to open given world file
    std::ifstream worldFile(argv[1]);
    if (!worldFile) {
        std::cerr << argv[1] << ": " << std::strerror(errno) << std::endl;
        return EXIT_FAILURE;
    }

    // try to open given source file
    std::ifstream sourceFile(argv[2]);
    if (!sourceFile) {
        std::cerr << argv[2] << ": " << std::strerror(errno) << std::endl;
        return EXIT_FAILURE;
    }

    // create the interpret
    Interpret interpret(worldFile, sourceFile);

    // run the program
    unsigned steps = interpret.run();
    std::cout << "Program finished in " << steps << " steps.\n";

    // print out the world
    const auto& world = interpret.world();
    const auto& robot = interpret.robot();

    std::cout << '+' << std::string(world.width(), '-') << "+\n";

    for (int y = 0; static_cast<unsigned>(y) < world.height(); ++y) {
        std::cout << '|';

        for (int x = 0; static_cast<unsigned>(x) < world.width(); ++x) {
            const auto& tile = world.tile({ x, y });

            if (robot.position().x == x && robot.position().y == y) {
                char dir;
                switch (robot.direction()) {
                case Direction::North: dir = 'n'; break;
                case Direction::East:  dir = 'e'; break;
                case Direction::South: dir = 's'; break;
                case Direction::West:  dir = 'w'; break;
                }

                if (tile.marks)
                    dir = std::toupper(dir);

                std::cout << dir;
            } else if (tile.marks > 9u) {
                std::cout << '*';
            } else if (tile.marks > 0u) {
                std::cout << tile.marks;
            } else if (tile.wall) {
                std::cout << '#';
            } else {
                std::cout << ' ';
            }
        }

        std::cout << "|\n";
    }

    std::cout << '+' << std::string(world.width(), '-') << "+\n";

    // that's it apparently
    return EXIT_SUCCESS;
}
