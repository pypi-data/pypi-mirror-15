/*
*   Copyright (c) 2010-2016, MIT Probabilistic Computing Project
*
*   Lead Developers: Dan Lovell and Jay Baxter
*   Authors: Dan Lovell, Baxter Eaves, Jay Baxter, Vikash Mansinghka
*   Research Leads: Vikash Mansinghka, Patrick Shafto
*
*   Licensed under the Apache License, Version 2.0 (the "License");
*   you may not use this file except in compliance with the License.
*   You may obtain a copy of the License at
*
*       http://www.apache.org/licenses/LICENSE-2.0
*
*   Unless required by applicable law or agreed to in writing, software
*   distributed under the License is distributed on an "AS IS" BASIS,
*   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*   See the License for the specific language governing permissions and
*   limitations under the License.
*/
#include <iostream>
#include <vector>
#include "ComponentModel.h"
#include "ContinuousComponentModel.h"
#include "MultinomialComponentModel.h"

using namespace std;

int main() {
    cout << "Hello World" << endl;

    map<string, double> continuous_hypers;
    continuous_hypers["r"] = 10;
    continuous_hypers["nu"] = 10;
    continuous_hypers["s"] = 10;
    continuous_hypers["mu"] = 10;
    map<string, double> multinomial_hypers;
    multinomial_hypers["K"] = 10;
    multinomial_hypers["dirichlet_alpha"] = 10;

    // container of pointers with memory management
    ContinuousComponentModel *p_ccm = new ContinuousComponentModel(
        continuous_hypers);
    MultinomialComponentModel *p_mcm = new MultinomialComponentModel(
        multinomial_hypers);
    vector<ComponentModel*> p_cm_v;
    p_cm_v.push_back(p_ccm);
    p_cm_v.push_back(p_mcm);
    p_cm_v[0]->insert_element(9);
    p_cm_v[1]->insert_element(9);
    cout << "p_cm_v[0]->calc_marginal_logp(): " << p_cm_v[0]->calc_marginal_logp()
         << endl;
    cout << "p_cm_v[1]->calc_marginal_logp(): " << p_cm_v[1]->calc_marginal_logp()
         << endl;

    while (p_cm_v.size() != 0) {
        ComponentModel *p_cm = p_cm_v.back();
        cout << "*p_cm_v[i]: " << *p_cm << endl;
        cout << "p_cm->get_hypers(): " << p_cm->get_hypers() << endl;
        delete p_cm;
        p_cm_v.pop_back();
    }

    cout << "Goodbye World" << endl;
}
