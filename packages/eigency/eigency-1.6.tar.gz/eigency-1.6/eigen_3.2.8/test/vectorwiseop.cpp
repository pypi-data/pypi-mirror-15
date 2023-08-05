// This file is part of Eigen, a lightweight C++ template library
// for linear algebra.
//
// Copyright (C) 2011 Benoit Jacob <jacob.benoit.1@gmail.com>
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

#define EIGEN_NO_STATIC_ASSERT

#include "main.h"

template<typename ArrayType> void vectorwiseop_array(const ArrayType& m)
{
  typedef typename ArrayType::Index Index;
  typedef typename ArrayType::Scalar Scalar;
  typedef Array<Scalar, ArrayType::RowsAtCompileTime, 1> ColVectorType;
  typedef Array<Scalar, 1, ArrayType::ColsAtCompileTime> RowVectorType;

  Index rows = m.rows();
  Index cols = m.cols();
  Index r = internal::random<Index>(0, rows-1),
        c = internal::random<Index>(0, cols-1);

  ArrayType m1 = ArrayType::Random(rows, cols),
            m2(rows, cols),
            m3(rows, cols);

  ColVectorType colvec = ColVectorType::Random(rows);
  RowVectorType rowvec = RowVectorType::Random(cols);

  // test addition

  m2 = m1;
  m2.colwise() += colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() + colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) + colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() += colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() + colvec.transpose());

  m2 = m1;
  m2.rowwise() += rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() + rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) + rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() += rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() + rowvec.transpose());

  // test substraction

  m2 = m1;
  m2.colwise() -= colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() - colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) - colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() -= colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() - colvec.transpose());

  m2 = m1;
  m2.rowwise() -= rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() - rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) - rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() -= rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() - rowvec.transpose());

  // test multiplication

  m2 = m1;
  m2.colwise() *= colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() * colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) * colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() *= colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() * colvec.transpose());

  m2 = m1;
  m2.rowwise() *= rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() * rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) * rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() *= rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() * rowvec.transpose());

  // test quotient

  m2 = m1;
  m2.colwise() /= colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() / colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) / colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() /= colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() / colvec.transpose());

  m2 = m1;
  m2.rowwise() /= rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() / rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) / rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() /= rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() / rowvec.transpose());
  
  m2 = m1;
  // yes, there might be an aliasing issue there but ".rowwise() /="
  // is suppposed to evaluate " m2.colwise().sum()" into to temporary to avoid
  // evaluating the reducions multiple times
  if(ArrayType::RowsAtCompileTime>2 || ArrayType::RowsAtCompileTime==Dynamic)
  {
    m2.rowwise() /= m2.colwise().sum();
    VERIFY_IS_APPROX(m2, m1.rowwise() / m1.colwise().sum());
  }

  // all/any
  Array<bool,Dynamic,Dynamic> mb(rows,cols);
  mb = (m1.real()<=0.7).colwise().all();
  VERIFY( (mb.col(c) == (m1.real().col(c)<=0.7).all()).all() );
  mb = (m1.real()<=0.7).rowwise().all();
  VERIFY( (mb.row(r) == (m1.real().row(r)<=0.7).all()).all() );

  mb = (m1.real()>=0.7).colwise().any();
  VERIFY( (mb.col(c) == (m1.real().col(c)>=0.7).any()).all() );
  mb = (m1.real()>=0.7).rowwise().any();
  VERIFY( (mb.row(r) == (m1.real().row(r)>=0.7).any()).all() );
}

template<typename MatrixType> void vectorwiseop_matrix(const MatrixType& m)
{
  typedef typename MatrixType::Index Index;
  typedef typename MatrixType::Scalar Scalar;
  typedef typename NumTraits<Scalar>::Real RealScalar;
  typedef Matrix<Scalar, MatrixType::RowsAtCompileTime, 1> ColVectorType;
  typedef Matrix<Scalar, 1, MatrixType::ColsAtCompileTime> RowVectorType;
  typedef Matrix<RealScalar, MatrixType::RowsAtCompileTime, 1> RealColVectorType;
  typedef Matrix<RealScalar, 1, MatrixType::ColsAtCompileTime> RealRowVectorType;

  Index rows = m.rows();
  Index cols = m.cols();
  Index r = internal::random<Index>(0, rows-1),
        c = internal::random<Index>(0, cols-1);

  MatrixType m1 = MatrixType::Random(rows, cols),
            m2(rows, cols),
            m3(rows, cols);

  ColVectorType colvec = ColVectorType::Random(rows);
  RowVectorType rowvec = RowVectorType::Random(cols);
  RealColVectorType rcres;
  RealRowVectorType rrres;

  // test addition

  m2 = m1;
  m2.colwise() += colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() + colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) + colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() += colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() + colvec.transpose());

  m2 = m1;
  m2.rowwise() += rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() + rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) + rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() += rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() + rowvec.transpose());

  // test substraction

  m2 = m1;
  m2.colwise() -= colvec;
  VERIFY_IS_APPROX(m2, m1.colwise() - colvec);
  VERIFY_IS_APPROX(m2.col(c), m1.col(c) - colvec);

  VERIFY_RAISES_ASSERT(m2.colwise() -= colvec.transpose());
  VERIFY_RAISES_ASSERT(m1.colwise() - colvec.transpose());

  m2 = m1;
  m2.rowwise() -= rowvec;
  VERIFY_IS_APPROX(m2, m1.rowwise() - rowvec);
  VERIFY_IS_APPROX(m2.row(r), m1.row(r) - rowvec);

  VERIFY_RAISES_ASSERT(m2.rowwise() -= rowvec.transpose());
  VERIFY_RAISES_ASSERT(m1.rowwise() - rowvec.transpose());
  
  // test norm
  rrres = m1.colwise().norm();
  VERIFY_IS_APPROX(rrres(c), m1.col(c).norm());
  rcres = m1.rowwise().norm();
  VERIFY_IS_APPROX(rcres(r), m1.row(r).norm());
  
  // test normalized
  m2 = m1.colwise().normalized();
  VERIFY_IS_APPROX(m2.col(c), m1.col(c).normalized());
  m2 = m1.rowwise().normalized();
  VERIFY_IS_APPROX(m2.row(r), m1.row(r).normalized());
  
  // test normalize
  m2 = m1;
  m2.colwise().normalize();
  VERIFY_IS_APPROX(m2.col(c), m1.col(c).normalized());
  m2 = m1;
  m2.rowwise().normalize();
  VERIFY_IS_APPROX(m2.row(r), m1.row(r).normalized());
}

void test_vectorwiseop()
{
  CALL_SUBTEST_1(vectorwiseop_array(Array22cd()));
  CALL_SUBTEST_2(vectorwiseop_array(Array<double, 3, 2>()));
  CALL_SUBTEST_3(vectorwiseop_array(ArrayXXf(3, 4)));
  CALL_SUBTEST_4(vectorwiseop_matrix(Matrix4cf()));
  CALL_SUBTEST_5(vectorwiseop_matrix(Matrix<float,4,5>()));
  CALL_SUBTEST_6(vectorwiseop_matrix(MatrixXd(7,2)));
}
