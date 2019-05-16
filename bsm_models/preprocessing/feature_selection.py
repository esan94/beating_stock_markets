from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif


def fit_transform_features(feature_selection, feat_train_values, target_train_values,
                           feat_test_values, target_test_values):

    if feature_selection == 'f_classif':
        bests = SelectKBest(f_classif, k=20)
        feat_train_values = bests.fit_transform(feat_train_values, target_train_values)
        feat_test_values = bests.fit_transform(feat_test_values, target_test_values)
    elif feature_selection == 'mutual':
        bests = SelectKBest(mutual_info_classif, k=20)
        feat_train_values = bests.fit_transform(feat_train_values, target_train_values)
        feat_test_values = bests.fit_transform(feat_test_values, target_test_values)

    else:
        feat_train_values = feat_train_values
        feat_test_values = feat_test_values

    return feat_train_values, feat_test_values
