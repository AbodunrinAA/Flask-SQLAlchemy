import datetime

from flask_restful import inputs, reqparse

# StoreModel Parser
storeParser = reqparse.RequestParser()
storeParser.add_argument('name',
                         type=str,
                         required=True,
                         help='Store Name is required.'
                         )
storeParser.add_argument('address',
                         type=str,
                         required=True,
                         help='Store Address is required.'
                         )
storeParser.add_argument('number',
                         type=str,
                         required=True,
                         help='Store Number is required.'
                         )
storeParser.add_argument('email',
                         type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
                         action='append',
                         required=True,
                         help='Supply Valid Email Address.'
                         )
storeParser.add_argument('business_id',
                         type=str,
                         required=True,
                         help='Business_Id is required.'
                         )

# Item Parser
itemParser = reqparse.RequestParser()
itemParser.add_argument('name',
                        type=str,
                        required=True,
                        help='Item Name is required'
                        )
itemParser.add_argument('produce_date',
                        type=str,
                        required=True,
                        help='Date of produce is required'
                        )
itemParser.add_argument('expire_date',
                        type=str,
                        required=True,
                        help='Item Price is required'
                        )
itemParser.add_argument('price',
                        type=int,
                        required=True,
                        help='Item Price is required'
                        )
itemParser.add_argument('store_id',
                        type=str,
                        required=True,
                        help='Store_id is required'
                        )

# User Parser
userParser = reqparse.RequestParser()
userParser.add_argument('username',
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
                        action='append',
                        required=True,
                        help='Username should be a valid Email Address'
                        )
userParser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required'
                        )
userParser.add_argument('role',
                        type=str,
                        required=False
                        )

userParser.add_argument('firstname',
                        type=str,
                        required=False
                        )
userParser.add_argument('lastname',
                        type=str,
                        required=False
                        )
userParser.add_argument('store_id',
                        type=str,
                        required=True,
                        help='Business_Id is required.'
                        )

# BusinessModer Parser
businessParser = reqparse.RequestParser()
businessParser.add_argument('name',
                            type=str,
                            required=True,
                            help='Business Name is required.'
                            )
businessParser.add_argument('address',
                            type=str,
                            required=True,
                            help='Business Address is required.'
                            )

# Transaction Parser
transactionParser = reqparse.RequestParser()
transactionParser.add_argument('itemId',
                               type=str,
                               required=True,
                               help='Item Id is required.'
                               )

#
creditScoreParser = reqparse.RequestParser()
creditScoreParser.add_argument('business_id',
                               type=str,
                               required=True,
                               help='Business Id is required.'
                               )

transactionQueryParser = reqparse.RequestParser()
transactionQueryParser.add_argument('business_id',
                                    type=str,
                                    required=True,
                                    help='Business Id is required.'
                                    )
transactionQueryParser.add_argument('today',
                                    type=bool,
                                    required=True,
                                    help='today Id is required.'
                                    )
