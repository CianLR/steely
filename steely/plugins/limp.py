import sys
import limp
import limp.errors
import limp.environment


COMMAND = 'limp'
__author__ = 'byxor'


GLOBAL_DEFINITIONS = {}


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):

    def send(message):
        bot.sendMessage(str(message), thread_id=thread_id, thread_type=thread_type)

    def send_error(info, error):
        full_error_message = f'\n{type(error).__name__}: {error}'
        send(f'{info} {full_error_message}')

    def last_message():
        return bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1].text

    def define_global(name, variable):
        send("This is a hack; enjoy.")
        GLOBAL_DEFINITIONS[name] = variable

    try:
        environment = limp.environment.create_standard()

        _define([
            ('send', send),
            ('last-message', last_message),
            ('define-global', define_global),
        ] + GLOBAL_DEFINITIONS.items(), environment)

        result = limp.evaluate(source_code, environment)
        send(result)
    except limp.errors.LimpError as error:
        send_error('You got a limp error', error)
    except Exception as error:
        send_error('Something unexpected happened', error)
        send("It's possible that it's your fault.")


def _define(custom_symbols, environment):
    for name, value in custom_definitions:
        try:
            environment.define(name, value)
        except limp.errors.RedefinedSymbol:
            pass


def _generate_help():

    def _help():
        _FULL_COMMAND = f".{COMMAND}"
        _REPOSITORY = f"https://www.github.com/byxor/limp"
        _BORDER = '=' * 10

        def _CREATE_CODE_EXAMPLE(code):
            result = limp.evaluate(code)
            message = f"User: {_FULL_COMMAND} {code}"
            response = f"ChatBot: {result}"
            return message + "\n" + response + "\n\n"

        _CREATE_CODE_EXAMPLES = lambda input_examples: "".join(list(map(_CREATE_CODE_EXAMPLE, input_examples))).strip()

        description = "Evaluate the limp programming language!"
        usage = f"Usage: {_FULL_COMMAND} <source_code>"
        examples = _CREATE_CODE_EXAMPLES([
            "(+ 1 2)",
            "(// 100 (- 5 2))",
            "((x -> (* x 2)) 10)",
            "((x -> (* x 2)) 50)",
            "(map (name -> (concatenate \"hi, \" name)) [\"john\" \"jane\" \"bob\"])",
            "(do\n (define add (a b -> (+ a b)))\n (add 30 70))",
        ])
        source_code = f"Source code: {_REPOSITORY}"
        contributing = f"Want to contribute? Awesome! Make sure you read CONTRIBUTING.md in the repository first."

        return "\n\n".join([
            description,
            usage,
            _BORDER,
            examples,
            _BORDER,
            source_code,
            contributing,
        ])

    try:
        message = _help()
    except Exception as e:
        global __doc__
        message = "The help could not be autogenerated. It's possible that the code examples are outdated and aren't valid syntax anymore. Please inform Brandon."
        message += "\n\n"
        message += f"Reason: {e}"

    sys.modules[__name__].__doc__ = message


_generate_help()
