Solving a CAPTCHA
-----------------

Both of these scripts can be adapted for a variety of different applications.

This script will open a new Firefox window, go to Solve Media's demo page and
continuously solve it until it gets it right.

	#!/usr/bin/env python
	from caboodle import web, solve
	import time

	# Create the browser and solver
	browser = web.Browser('Firefox')
	solver = solve.captcha(browser, user = True)
	browser.get('http://solvemedia.com/advertisers/captcha-type-in')

	# Solve the CAPTCHA
	while True:
		solver.solve()
		browser.find_element_by_id('verify_engaging').click()

		try:
			browser.find_element_by_id('engaging-incorrect')
		except:
			break

		solver.invalid()

	# Wait and quit
	time.sleep(5)
	browser.quit()

This script will open a new Firefox window, go to Google's reCAPTCHA demo page
and continuously solve it until it gets it right.

	#!/usr/bin/env python
	from caboodle import web, solve
	import time

	# Create the browser
	browser = web.Browser('Firefox')
	solver = solve.captcha(browser, online = ['rucaptcha', 'YOUR API KEY'])
	browser.get('https://www.google.com/recaptcha/api2/demo')

	# Solve the CAPTCHA
	while True:
		solver.solve()
		browser.find_element_by_tag_name('form').submit()

		try:
			browser.find_element_by_class_name('recaptcha-error-message')
		except:
			break

		solver.invalid()

	# Wait and quit
	time.sleep(5)
	browser.quit()
