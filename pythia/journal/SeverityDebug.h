// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Michael A.G. Aivazis
//                      California Institute of Technology
//                      (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#if !defined(pythia_journal_SeverityDebug_h)
#define pythia_journal_SeverityDebug_h


// forward declarations
namespace pythia {
    namespace journal {
        class Diagnostic;
        class SeverityDebug;
    }
}


class pythia::journal::SeverityDebug : public pythia::journal::Diagnostic {

// interface
public:
    string_t name() const { return  "debug." + facility(); }

// meta-methods
public:
    ~SeverityDebug() {}
    
    SeverityDebug(string_t name) :
        Diagnostic(name, "debug") {}

// disable these
private:
    SeverityDebug(const SeverityDebug &);
    const SeverityDebug & operator=(const SeverityDebug &);
};


#endif
// version
// $Id: SeverityDebug.h,v 1.1.1.1 2005/03/08 16:13:55 aivazis Exp $

// End of file 
