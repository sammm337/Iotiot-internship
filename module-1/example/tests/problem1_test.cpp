/**
 * @file problem1_test.cpp
 * @brief Test files for the example
 */
#include <gtest/gtest.h>
#include "problem1.h"

/**
 * @brief Construct a new TEST object for Testing Add function
 * 
 */
TEST(Problem1Test, Add) {
    /* Test 1 */
    ASSERT_EQ(2, add(1, 1));
    /* Test 2 */
    ASSERT_EQ(5, add(3, 2));
    /* Test 3 */
    ASSERT_EQ(10, add(7, 3));
}
/**
 * @brief Construct a new TEST object for Testing Sub function
 * 
 */
TEST(Problem1Test, Sub) {
    /* Test 1 */
    ASSERT_EQ(3, sub(5, 2));
    /* Test 2 */
    ASSERT_EQ(-10, sub(5, 15));
}

int main(int argc, char **argv) {
    /* Call the Google Testing framework */
    testing::InitGoogleTest(&argc, argv);
    /* Run all the tests */
    return RUN_ALL_TESTS();
}