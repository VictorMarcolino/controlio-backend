controller_base = """

#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <string>
#include <list>
using namespace std;

class Actuator
{
protected:
    int pin;
    bool state = false;

public:
    string identifier;
    string name;

    Actuator(int pin, string identifier, string name)
    {
        this->pin = pin;
        this->identifier = identifier;
        this->name = name;
    }

    virtual void do_action() = 0;

    string toJson()
    {
        string json = "{";
        json += "\\"identifier\\": \\"" + this->identifier + "\\",";
        json += "\\"name\\": \\"" + this->name + "\\",";
        json += "\\"state\\": ";
        json += (this->state ? "true" : "false");
        json += "}";
        return json;
    }
};

class MicroController {
private:
    list<Actuator *> listOfActuators;
    string controllerIp = "";

public:
    MicroController(list<Actuator *> actuators) {
        listOfActuators = std::move(actuators);
    }

    void setIP(string currentIp) {
        this->controllerIp = currentIp;
    }

    bool actuatorExists(string identifier) {
        for (std::list<Actuator *>::iterator it = this->listOfActuators.begin();
             it != this->listOfActuators.end(); ++it) {
            if ((*it)->identifier == identifier) {
                return true;
            }
        }
        return false;
    }

    string toJson() {

        string res = (this->controllerIp.length() == 0) ? "{\\"actuators\\": [" : "{\\"host\\": \\"" + this->controllerIp +
                                                                                "\\", \\"actuators\\": [";
        for (std::list<Actuator *>::iterator it = this->listOfActuators.begin();
             it != this->listOfActuators.end(); ++it) {
            res += (*it)->toJson();
            it++;
            if (it != this->listOfActuators.end()) {
                res += ",";
            }
            it--;
        }
        res += "]}";
        return res;
    }

    string toJson(string identifier) {
        for (std::list<Actuator *>::iterator it = this->listOfActuators.begin();
             it != this->listOfActuators.end(); ++it) {
            if ((*it)->identifier == identifier) {
                return (*it)->toJson();
            }
        }
        return "{}";
    }

    void trigger(string identifier) {
        for (std::list<Actuator *>::iterator it = this->listOfActuators.begin();
             it != this->listOfActuators.end(); ++it) {
            if ((*it)->identifier == identifier) {
                (*it)->do_action();
            }
        }
    }
};

enum Actions
{
    ListActuators,
    GetActuator,
    TriggerActuator
};

struct ActionIdentifier
{
    int action;
    string identifier;
};

class ControlioBoaderController : public MicroController
{

public:
    ControlioBoaderController(list<Actuator *> actuators) : MicroController(std::move(actuators)) {}

    ActionIdentifier extract_action_and_identifier_from_requested_url(string url)
    {
        int initpos = url.find("GET");
        int action = atoi(url.substr(initpos + 3 + 1 + 1, 1).c_str());

        if (action == 0)
        {
            return {action, "NOT NEEDED"};
        }
        string identifier = url.substr(initpos + 3 + 1 + 1 + 2, 36);
        return {action, identifier};
    };

    string responseSuccessWith(const string &response)
    {
        string res = "HTTP/1.1 200 OK\\r\\nContent-Type: application/json\\r\\n\\r\\n";
        res = res + response;
        return res;
    };

    string responseNotFound()
    {
        string res = "HTTP/1.1 404 Not Found\\r\\nContent-Type: application/json\\r\\n\\r\\n{\\"status\\" : 404}";
        return res;
    };

    string badRequest()
    {
        string res = "HTTP/1.1 400 Bad Request\\r\\nContent-Type: application/json\\r\\n\\r\\n{\\"status\\" : 400}";
        return res;
    };

    string main(const string &url)
    {
        struct ActionIdentifier actionIdentifier;
        actionIdentifier = this->extract_action_and_identifier_from_requested_url(url);
        switch (actionIdentifier.action)
        {
        case ListActuators:
            return this->responseSuccessWith(this->toJson());
            break;
        case GetActuator:
            if (this->actuatorExists(actionIdentifier.identifier))
            {
                return this->responseSuccessWith(this->toJson(actionIdentifier.identifier));
            }
            else
            {
                return this->responseNotFound();
            }
            break;
        case TriggerActuator:
            if (this->actuatorExists(actionIdentifier.identifier))
            {
                this->trigger(actionIdentifier.identifier);
                return this->responseSuccessWith(this->toJson(actionIdentifier.identifier));
            }
            else
            {
                return this->responseNotFound();
            }
            break;
        default:
            return this->badRequest();
        }
    }
};

#endif
"""
